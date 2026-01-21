from app.services.analyzer import check_tone_of_voice_ai

def test_informal_tone(monkeypatch):
    def fake_classifier(text):
        return [{"label": "negative", "score": 0.95}]

    monkeypatch.setattr(
        "app.services.analyzer.get_tone_classifier",
        lambda: fake_classifier
    )

    tone = check_tone_of_voice_ai("Wat een slecht idee!")
    assert tone == "informal"
