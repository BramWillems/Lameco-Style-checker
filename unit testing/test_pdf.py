from app.services.pdf_report import generate_pdf
import os

def test_pdf_is_created(tmp_path):
    dummy_ui = {
        "document": "test.docx",
        "created_at": "2026-01-01",
        "score": 80,
        "findings": []
    }

    out = tmp_path / "report.pdf"
    generate_pdf(dummy_ui, str(out))

    assert out.exists()
    assert out.stat().st_size > 0
