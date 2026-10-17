"""Load and save decks to a JSON file."""

import json
from pathlib import Path

DEFAULT_PATH = Path("data/cards.json")


def load_decks(path: Path = DEFAULT_PATH) -> dict[str, list[dict[str, str]]]:
    """Return all decks from the file, or an empty dict if it does not exist yet."""
    if not path.exists():
        return {}
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def save_decks(decks: dict[str, list[dict[str, str]]], path: Path = DEFAULT_PATH) -> None:
    """Write all decks to the file, creating its folder if needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(decks, f, ensure_ascii=False, indent=2)
