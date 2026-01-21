from app.services.analyzer import should_check_grammar

def test_short_bullet_is_ignored():
    assert should_check_grammar("Agenda") is False

def test_number_is_ignored():
    assert should_check_grammar("1") is False

def test_full_sentence_is_checked():
    assert should_check_grammar("Dit is een volledige zin.") is True
