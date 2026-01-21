# app/main.py - FIXED VERSION
import json
import uuid
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .db import (
    init_db,
    get_settings,
    update_settings,
    insert_analysis,
    list_analyses,
    get_analysis,
    update_analysis_pdf,
)

from .services.analyzer import analyze_document, normalize_to_ui
from .services.pdf_report import generate_pdf

UPLOAD_DIR = Path("data/uploads")
REPORT_DIR = Path("data/reports")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="Laméco AI Style Checker")

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.on_event("startup")
def _startup():
    init_db()

# -------------------------
# Pages
# -------------------------
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return RedirectResponse(url="/upload")

@app.get("/upload", response_class=HTMLResponse)
def upload_page(request: Request):
    s = get_settings()
    return templates.TemplateResponse("upload.html", {"request": request, "active": "upload", "settings": s})

@app.post("/upload")
async def upload_and_analyze(request: Request, file: UploadFile = File(...)):
    s = get_settings()
    ext = Path(file.filename).suffix.lower()
    if ext not in [".docx", ".pptx"]:
        return RedirectResponse(url="/upload?error=unsupported", status_code=303)

    analysis_id = str(uuid.uuid4())
    saved_path = UPLOAD_DIR / f"{analysis_id}_{file.filename}"
    content = await file.read()
    saved_path.write_bytes(content)

    # Import the new modules
    from .services.color_extractor import (
        extract_colors_docx, 
        extract_colors_pptx, 
        check_color_compliance
    )
    from .services.logo_detector import check_logo_compliance

    # Run analysis with ALL settings
    raw_report = analyze_document(
        str(saved_path),
        target_font=s["required_font_family"],
        check_fonts=bool(s["check_fonts"]),
        check_spelling=bool(s["check_spelling"]),
        check_tone=bool(s["check_tone"]),
        check_colors=bool(s["check_colors"]),  # NEW
        check_logo=bool(s["check_logo"]),      # NEW
    )
    
    # Add color checking if enabled
    if s["check_colors"]:
        if ext == ".docx":
            extracted_colors = extract_colors_docx(str(saved_path))
        else:  # .pptx
            extracted_colors = extract_colors_pptx(str(saved_path))
        
        color_issues = check_color_compliance(
            extracted_colors, 
            s["primary_color"]
        )
        raw_report["color_issues"] = color_issues
    
    # Add logo checking if enabled
    if s["check_logo"]:
        logo_issues = check_logo_compliance(
            str(saved_path),
            expected_position=s["logo_position"]
        )
        raw_report["logo_issues"] = logo_issues
    
    # Normalize to UI (with hyperlinks)
    ui_result = normalize_to_ui(raw_report, target_font=s["required_font_family"])

    # Save to DB
    created_at = datetime.now().isoformat()
    insert_analysis(
        analysis_id=analysis_id,
        filename=file.filename,
        created_at=created_at,
        result_json=json.dumps(ui_result, ensure_ascii=False),
        pdf_path=None
    )

    return RedirectResponse(url=f"/results/{analysis_id}", status_code=303)

@app.get("/results/{analysis_id}", response_class=HTMLResponse)
def results_page(request: Request, analysis_id: str):
    s = get_settings()
    row = get_analysis(analysis_id)
    if not row:
        return RedirectResponse(url="/upload", status_code=303)

    ui_result = json.loads(row["result_json"])
    return templates.TemplateResponse(
        "results.html",
        {"request": request, "active": "results", "settings": s, "analysis_id": analysis_id, "result": ui_result}
    )

@app.get("/reports", response_class=HTMLResponse)
def reports_page(request: Request):
    s = get_settings()
    rows = list_analyses()
    return templates.TemplateResponse(
        "reports.html",
        {"request": request, "active": "reports", "settings": s, "reports": rows}
    )

@app.get("/settings", response_class=HTMLResponse)
def settings_page(request: Request):
    s = get_settings()
    return templates.TemplateResponse("settings.html", {"request": request, "active": "settings", "settings": s})

@app.post("/settings")
def save_settings(
    primary_color: str = Form(...),
    required_font_family: str = Form(...),
    logo_position: str = Form(...),
    check_fonts: str = Form("off"),
    check_colors: str = Form("off"),
    check_logo: str = Form("off"),
    check_tone: str = Form("off"),
    check_spelling: str = Form("off"),
    email_notifications: str = Form("off"),
):
    new_s = {
        "primary_color": primary_color.strip(),
        "required_font_family": required_font_family.strip(),
        "logo_position": logo_position.strip(),
        "check_fonts": check_fonts == "on",
        "check_colors": check_colors == "on",
        "check_logo": check_logo == "on",
        "check_tone": check_tone == "on",
        "check_spelling": check_spelling == "on",
        "email_notifications": email_notifications == "on",
    }
    update_settings(new_s)
    return RedirectResponse(url="/settings?saved=1", status_code=303)

# -------------------------
# PDF export
# -------------------------
@app.get("/report/{analysis_id}/pdf")
def download_pdf(analysis_id: str):
    row = get_analysis(analysis_id)
    if not row:
        return RedirectResponse(url="/reports", status_code=303)

    ui_result = json.loads(row["result_json"])

    # If already generated, serve it
    if row.get("pdf_path"):
        p = Path(row["pdf_path"])
        if p.exists():
            return FileResponse(str(p), media_type="application/pdf", filename=f"{analysis_id}.pdf")

    out_path = REPORT_DIR / f"{analysis_id}.pdf"
    generate_pdf(ui_result, str(out_path))
    update_analysis_pdf(analysis_id, str(out_path))

    return FileResponse(str(out_path), media_type="application/pdf", filename=f"{analysis_id}.pdf")