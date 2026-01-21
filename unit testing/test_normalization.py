from app.services.analyzer import normalize_to_ui

def test_normalized_output_has_required_keys():
    dummy_report = {
        "bestand": "test.docx",
        "datum": "2026-01-01",
        "font_controle": [],
        "grammatica_fouten": []
    }

    ui = normalize_to_ui(dummy_report, target_font="Calibri")

    assert "score" in ui
    assert "findings" in ui
    assert "category_counts" in ui
