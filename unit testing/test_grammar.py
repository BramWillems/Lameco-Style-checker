from app.services.analyzer import analyze_document

def test_pptx_grammar_is_low_severity():
    report = analyze_document(
        "tests/fixtures/bullets.pptx",
        target_font="Calibri",
        check_spelling=True
    )
    assert "grammatica_fouten" in report
