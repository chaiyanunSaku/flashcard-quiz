from flashcard_quiz.cli import main
from flashcard_quiz.storage import load_decks, save_decks

HIRAGANA = [{"front": "あ", "back": "a"}, {"front": "い", "back": "i"}, {"front": "う", "back": "u"}]
KANJI = [{"front": "水", "back": "みず"}, {"front": "火", "back": "ひ"}]


def run_app(monkeypatch, path, typed):
    """Run the menu as if the user typed each item in `typed`, with cards in saved order."""
    answers = iter(typed)
    monkeypatch.setattr("builtins.input", lambda prompt="": next(answers))
    main(path=path, shuffle=lambda cards: None)


def test_quiz_marks_answers_and_shows_score(tmp_path, monkeypatch, capsys):
    # C1
    path = tmp_path / "cards.json"
    save_decks({"Hiragana": HIRAGANA}, path)

    run_app(monkeypatch, path, ["start", "1", "a", " I ", "o", "exit"])

    out = capsys.readouterr().out
    assert out.count("Correct!") == 2
    assert "Wrong. Answer: u" in out
    assert "Score: 2/3" in out


def test_answering_n_keeps_the_deck(tmp_path, monkeypatch):
    # C6
    path = tmp_path / "cards.json"
    save_decks({"Kanji": KANJI}, path)

    run_app(monkeypatch, path, ["delete", "deck", "1", "n", "exit"])

    assert load_decks(path) == {"Kanji": KANJI}


def test_answering_y_deletes_the_deck_for_good(tmp_path, monkeypatch, capsys):
    # C7
    path = tmp_path / "cards.json"
    save_decks({"Hiragana": HIRAGANA, "Kanji": KANJI}, path)

    run_app(monkeypatch, path, ["delete", "deck", "2", "y", "exit"])
    capsys.readouterr()  # forget the output so far

    # Restart the app and open the deck list for a quiz.
    run_app(monkeypatch, path, ["start", "9", "exit"])

    out = capsys.readouterr().out
    assert "Hiragana" in out
    assert "Kanji" not in out
    assert load_decks(path) == {"Hiragana": HIRAGANA}


def test_empty_deck_returns_to_menu(tmp_path, monkeypatch, capsys):
    # C8
    path = tmp_path / "cards.json"
    save_decks({"Katakana": []}, path)

    run_app(monkeypatch, path, ["start", "1", "exit"])

    out = capsys.readouterr().out
    assert "This deck has no cards yet." in out
    assert "Bye!" in out  # the menu kept running until "exit"
