import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional

DB_PATH = Path("data/app.db")

def get_conn() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS analyses (
        id TEXT PRIMARY KEY,
        filename TEXT NOT NULL,
        created_at TEXT NOT NULL,
        result_json TEXT NOT NULL,
        pdf_path TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        id INTEGER PRIMARY KEY CHECK (id = 1),
        primary_color TEXT NOT NULL,
        required_font_family TEXT NOT NULL,
        logo_position TEXT NOT NULL,
        check_fonts INTEGER NOT NULL,
        check_colors INTEGER NOT NULL,
        check_logo INTEGER NOT NULL,
        check_tone INTEGER NOT NULL,
        check_spelling INTEGER NOT NULL,
        email_notifications INTEGER NOT NULL
    )
    """)

    # Insert default settings if not exists
    cur.execute("SELECT COUNT(*) as c FROM settings WHERE id=1")
    if cur.fetchone()["c"] == 0:
        cur.execute("""
        INSERT INTO settings (
            id, primary_color, required_font_family, logo_position,
            check_fonts, check_colors, check_logo, check_tone, check_spelling,
            email_notifications
        ) VALUES (
            1, '#1A3CE0', 'Calibri', 'Top Right',
            1, 1, 1, 1, 1,
            0
        )
        """)

    conn.commit()
    conn.close()

def get_settings() -> Dict[str, Any]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM settings WHERE id=1")
    row = cur.fetchone()
    conn.close()

    return dict(row)

def update_settings(new_settings: Dict[str, Any]) -> None:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    UPDATE settings SET
        primary_color=?,
        required_font_family=?,
        logo_position=?,
        check_fonts=?,
        check_colors=?,
        check_logo=?,
        check_tone=?,
        check_spelling=?,
        email_notifications=?
    WHERE id=1
    """, (
        new_settings["primary_color"],
        new_settings["required_font_family"],
        new_settings["logo_position"],
        int(new_settings["check_fonts"]),
        int(new_settings["check_colors"]),
        int(new_settings["check_logo"]),
        int(new_settings["check_tone"]),
        int(new_settings["check_spelling"]),
        int(new_settings["email_notifications"]),
    ))
    conn.commit()
    conn.close()

def insert_analysis(analysis_id: str, filename: str, created_at: str, result_json: str, pdf_path: Optional[str]) -> None:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO analyses (id, filename, created_at, result_json, pdf_path)
    VALUES (?, ?, ?, ?, ?)
    """, (analysis_id, filename, created_at, result_json, pdf_path))
    conn.commit()
    conn.close()

def list_analyses() -> List[Dict[str, Any]]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    SELECT id, filename, created_at, pdf_path
    FROM analyses
    ORDER BY created_at DESC
    """)
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_analysis(analysis_id: str) -> Optional[Dict[str, Any]]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM analyses WHERE id=?", (analysis_id,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None

def update_analysis_pdf(analysis_id: str, pdf_path: str) -> None:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE analyses SET pdf_path=? WHERE id=?", (pdf_path, analysis_id))
    conn.commit()
    conn.close()
