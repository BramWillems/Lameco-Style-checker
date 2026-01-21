from app.services.analyzer import analyze_document

def test_font_check_can_be_disabled():
    report = analyze_document(
        "tests/fixtures/wrong_font.docx",
        target_font="Calibri",
        check_fonts=False
    )
    assert report["font_controle"] == []
