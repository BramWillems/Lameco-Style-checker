from app.services.analyzer import check_font_consistency_docx

def test_correct_font_has_no_errors():
    result = check_font_consistency_docx(
        "tests/fixtures/correct_font.docx",
        target_font="Calibri"
    )
    assert result == []

def test_wrong_font_is_detected():
    result = check_font_consistency_docx(
        "tests/fixtures/wrong_font.docx",
        target_font="Calibri"
    )
    assert len(result) > 0
    assert result[0]["font_expected"] == "Calibri"
