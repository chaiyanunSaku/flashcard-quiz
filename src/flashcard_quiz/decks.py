"""Rules for creating, editing and deleting decks and cards.

Every function changes the given decks dict in place. A broken rule raises
ValueError with the message to show the user, and nothing is changed.
"""

from flashcard_quiz.quiz import accepted_answers

Decks = dict[str, list[dict[str, str]]]


def _get_deck(decks: Decks, name: str) -> list[dict[str, str]]:
    if name not in decks:
        raise ValueError(f"Deck '{name}' not found.")
    return decks[name]


def _get_card(decks: Decks, deck_name: str, index: int) -> dict[str, str]:
    cards = _get_deck(decks, deck_name)
    if not 0 <= index < len(cards):
        raise ValueError("Invalid choice.")
    return cards[index]


def _clean_card_text(text: str) -> str:
    text = text.strip()
    if not text:
        raise ValueError("Card cannot be empty!")
    return text


def _clean_back(text: str) -> str:
    # A back like " | " is not empty text, but it has no answer anyone could type.
    text = _clean_card_text(text)
    if not accepted_answers(text):
        raise ValueError("Card cannot be empty!")
    return text


def create_deck(decks: Decks, name: str) -> None:
    """Add an empty deck. Names are unique ignoring case."""
    name = name.strip()
    if not name:
        raise ValueError("Deck name cannot be empty!")
    for existing in decks:
        if existing.casefold() == name.casefold():
            raise ValueError(f"Deck '{existing}' already exists!")
    decks[name] = []


def add_card(decks: Decks, deck_name: str, front: str, back: str) -> None:
    """Add a card to the end of a deck."""
    cards = _get_deck(decks, deck_name)
    cards.append({"front": _clean_card_text(front), "back": _clean_back(back)})


def edit_card(
    decks: Decks, deck_name: str, index: int, front: str | None = None, back: str | None = None
) -> None:
    """Change a card's front, back or both. A side left as None stays the same."""
    card = _get_card(decks, deck_name, index)
    # Check both sides before changing anything, so a rejected edit leaves the card as it was.
    new_front = _clean_card_text(front) if front is not None else card["front"]
    new_back = _clean_back(back) if back is not None else card["back"]
    card["front"] = new_front
    card["back"] = new_back


def delete_card(decks: Decks, deck_name: str, index: int) -> None:
    """Remove one card from a deck."""
    _get_card(decks, deck_name, index)
    del decks[deck_name][index]


def delete_deck(decks: Decks, name: str) -> None:
    """Remove a whole deck and its cards. The CLI asks for confirmation first."""
    _get_deck(decks, name)
    del decks[name]
