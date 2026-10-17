from flashcard_quiz.storage import load_decks, save_decks


def test_saved_decks_are_loaded_back(tmp_path):
    path = tmp_path / "cards.json"
    decks = {
        "Kanji": [{"front": "水", "back": "みず"}, {"front": "食べる", "back": "たべる|食べる"}],
        "Katakana": [],
    }

    save_decks(decks, path)

    assert load_decks(path) == decks


def test_missing_file_gives_no_decks(tmp_path):
    assert load_decks(tmp_path / "missing.json") == {}


def test_japanese_is_saved_as_readable_text(tmp_path):
    path = tmp_path / "cards.json"

    save_decks({"Kanji": [{"front": "水", "back": "みず"}]}, path)

    assert "みず" in path.read_text(encoding="utf-8")
