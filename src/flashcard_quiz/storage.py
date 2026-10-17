"""Load and save decks to a JSON file."""

import json
from pathlib import Path

DEFAULT_PATH = Path("data/cards.json")


def _is_valid(decks: object) -> bool:
    """Check the file holds {deck name: [{"front": text, "back": text}, ...]}."""
    return isinstance(decks, dict) and all(
        isinstance(cards, list)
        and all(
            isinstance(card, dict)
            and isinstance(card.get("front"), str)
            and isinstance(card.get("back"), str)
            for card in cards
        )
        for cards in decks.values()
    )


def load_decks(path: Path = DEFAULT_PATH) -> dict[str, list[dict[str, str]]]:
    """Return all decks from the file, or an empty dict if it does not exist yet.

    A file that cannot be read as decks raises ValueError, so it is never overwritten.
    """
    if not path.exists():
        return {}
    message = f"{path} is broken, so it was not loaded. Fix or delete it, then start again."
    try:
        with path.open(encoding="utf-8") as f:
            decks = json.load(f)
    except ValueError as error:  # not valid JSON, or not UTF-8 text
        raise ValueError(message) from error
    if not _is_valid(decks):
        raise ValueError(message)
    return decks


def save_decks(decks: dict[str, list[dict[str, str]]], path: Path = DEFAULT_PATH) -> None:
    """Write all decks to the file, creating its folder if needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(decks, f, ensure_ascii=False, indent=2)
