import pytest

from flashcard_quiz.decks import add_card, create_deck, delete_card, delete_deck, edit_card


def test_create_deck_adds_empty_deck():
    decks = {}

    create_deck(decks, "Kanji")

    assert decks == {"Kanji": []}


def test_duplicate_deck_name_is_rejected():
    # C2
    decks = {"Kanji": [{"front": "水", "back": "みず"}]}

    with pytest.raises(ValueError, match="already exists"):
        create_deck(decks, "Kanji")

    assert decks == {"Kanji": [{"front": "水", "back": "みず"}]}


def test_duplicate_deck_name_ignores_case():
    decks = {"Kanji": []}

    with pytest.raises(ValueError, match="already exists"):
        create_deck(decks, "kanji")

    assert list(decks) == ["Kanji"]


def test_add_card_with_empty_back_is_rejected():
    decks = {"Kanji": []}

    with pytest.raises(ValueError, match="Card cannot be empty!"):
        add_card(decks, "Kanji", "水", "   ")

    assert decks == {"Kanji": []}


@pytest.mark.parametrize("side", ["front", "back"])
def test_edit_to_empty_is_rejected_and_card_unchanged(side):
    # C4
    decks = {"Kanji": [{"front": "水", "back": "みず"}]}

    with pytest.raises(ValueError, match="Card cannot be empty!"):
        edit_card(decks, "Kanji", 0, **{side: ""})

    assert decks["Kanji"][0] == {"front": "水", "back": "みず"}


def test_edit_back_changes_only_back():
    # C5 (edit part)
    decks = {"Kanji": [{"front": "水", "back": "みず"}]}

    edit_card(decks, "Kanji", 0, back="みず|すい")

    assert decks["Kanji"][0] == {"front": "水", "back": "みず|すい"}


def test_delete_card_removes_only_that_card():
    decks = {"Kanji": [{"front": "水", "back": "みず"}, {"front": "火", "back": "ひ"}]}

    delete_card(decks, "Kanji", 0)

    assert decks["Kanji"] == [{"front": "火", "back": "ひ"}]


def test_delete_deck_removes_deck_and_its_cards():
    decks = {"Kanji": [{"front": "水", "back": "みず"}], "Hiragana": []}

    delete_deck(decks, "Kanji")

    assert decks == {"Hiragana": []}
