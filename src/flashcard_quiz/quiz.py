"""Rules for checking answers and scoring a quiz."""

import random
import unicodedata
from collections.abc import Callable


def normalize(text: str) -> str:
    """Ignore surrounding spaces (including full-width), letter case, and full-/half-width forms."""
    # NFKC turns full-width "ａ" into "a" and half-width "ｱ" into "ア", as typed with the IME on.
    return unicodedata.normalize("NFKC", text).strip().casefold()


def accepted_answers(back: str) -> list[str]:
    """Split a card's back into its accepted answers, e.g. 'たべる|食べる'."""
    # Treat the full-width bar "｜" (typed with the IME on) the same as "|".
    parts = back.replace("｜", "|").split("|")
    return [answer.strip() for answer in parts if answer.strip()]


def check_answer(answer: str, back: str) -> bool:
    """Return True if the answer matches any accepted answer on the card's back."""
    return normalize(answer) in [normalize(accepted) for accepted in accepted_answers(back)]


def shuffled_cards(
    cards: list[dict[str, str]], shuffle: Callable[[list], None] = random.shuffle
) -> list[dict[str, str]]:
    """Return the cards in a new random order. Tests pass their own shuffle to fix the order."""
    order = list(cards)
    shuffle(order)
    return order


def format_score(correct: int, total: int) -> str:
    """Return the score as correct/total, e.g. '8/10'."""
    return f"{correct}/{total}"
