"""Command-line menu. This is the only module that talks to the user."""

import random
import sys
from collections.abc import Callable
from pathlib import Path

from flashcard_quiz.decks import Decks, add_card, create_deck, delete_card, delete_deck, edit_card
from flashcard_quiz.quiz import accepted_answers, check_answer, format_score, shuffled_cards
from flashcard_quiz.storage import DEFAULT_PATH, load_decks, save_decks

BANNER = "勉強しよう！"
COMMANDS = """Commands:
  start   Quiz yourself on a deck
  list    Show all decks
  create  Create a new deck
  add     Add cards to a deck
  edit    Edit a card
  delete  Delete a deck or a card
  exit    Quit"""


def _use_utf8() -> None:
    """Let Japanese be printed and typed even if the terminal's default encoding cannot handle it."""
    for stream in (sys.stdin, sys.stdout):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")


def ask_yes_no(prompt: str) -> bool:
    return input(prompt).strip().casefold() == "y"


def choose(items: list[str], prompt: str) -> int | None:
    """Print a numbered list and return the chosen index, or None if the choice is invalid."""
    for number, item in enumerate(items, start=1):
        print(f"  {number}. {item}")
    choice = input(prompt).strip()
    if choice.isdecimal() and 1 <= int(choice) <= len(items):
        return int(choice) - 1
    print("Invalid choice.")
    return None


def choose_deck(decks: Decks) -> str | None:
    if not decks:
        print("No decks yet. Use 'create' to make one.")
        return None
    names = list(decks)
    index = choose(names, "Deck number: ")
    return None if index is None else names[index]


def choose_card(decks: Decks, deck_name: str) -> int | None:
    cards = decks[deck_name]
    if not cards:
        print("This deck has no cards yet.")
        return None
    return choose([f"{card['front']} → {card['back']}" for card in cards], "Card number: ")


def run_quiz(decks: Decks, shuffle: Callable[[list], None]) -> None:
    name = choose_deck(decks)
    if name is None:
        return
    cards = decks[name]
    if not cards:
        print("This deck has no cards yet.")
        return
    correct = 0
    for card in shuffled_cards(cards, shuffle):
        answer = input(f"{card['front']} → ")
        if check_answer(answer, card["back"]):
            print("Correct!")
            correct += 1
        else:
            print(f"Wrong. Answer: {' / '.join(accepted_answers(card['back']))}")
    print(f"Score: {format_score(correct, len(cards))}")


def list_decks(decks: Decks) -> None:
    if not decks:
        print("No decks yet. Use 'create' to make one.")
    for name, cards in decks.items():
        print(f"  {name} ({len(cards)} {'card' if len(cards) == 1 else 'cards'})")


def add_cards(decks: Decks, deck_name: str, path: Path) -> None:
    while ask_yes_no("Add a card? (y/n): "):
        front = input("Front: ")
        back = input("Back (use | between alternatives): ")
        try:
            add_card(decks, deck_name, front, back)
        except ValueError as error:
            print(error)
            continue
        save_decks(decks, path)
        print("Card added.")


def create_new_deck(decks: Decks, path: Path) -> None:
    name = input("Deck name: ").strip()
    try:
        create_deck(decks, name)
    except ValueError as error:
        print(error)
        return
    save_decks(decks, path)
    print(f"Deck '{name}' created.")
    add_cards(decks, name, path)


def add_to_deck(decks: Decks, path: Path) -> None:
    name = choose_deck(decks)
    if name is not None:
        add_cards(decks, name, path)


def edit_a_card(decks: Decks, path: Path) -> None:
    name = choose_deck(decks)
    if name is None:
        return
    index = choose_card(decks, name)
    if index is None:
        return
    side = input("Edit front, back or both? ").strip().casefold()
    if side not in ("front", "back", "both"):
        print("Invalid choice.")
        return
    front = input("New front: ") if side in ("front", "both") else None
    back = input("New back: ") if side in ("back", "both") else None
    try:
        edit_card(decks, name, index, front=front, back=back)
    except ValueError as error:
        print(error)
        return
    save_decks(decks, path)
    print("Card updated.")


def delete_something(decks: Decks, path: Path) -> None:
    kind = input("Delete deck or card? ").strip().casefold()
    if kind == "deck":
        name = choose_deck(decks)
        if name is None:
            return
        if not ask_yes_no(f"Delete deck '{name}' and all its cards? (y/n): "):
            print("Cancelled.")
            return
        delete_deck(decks, name)
        save_decks(decks, path)
        print(f"Deck '{name}' deleted.")
    elif kind == "card":
        name = choose_deck(decks)
        if name is None:
            return
        index = choose_card(decks, name)
        if index is None:
            return
        delete_card(decks, name, index)
        save_decks(decks, path)
        print("Card deleted.")
    else:
        print("Invalid choice.")


def main(path: Path = DEFAULT_PATH, shuffle: Callable[[list], None] = random.shuffle) -> None:
    """Run the menu until the user types exit. Tests pass their own path and shuffle."""
    _use_utf8()
    try:
        decks = load_decks(path)
    except ValueError as error:
        print(error)
        return
    print(BANNER)
    print(COMMANDS)
    try:
        while True:
            command = input("\n> ").strip().casefold()
            if command == "start":
                run_quiz(decks, shuffle)
            elif command == "list":
                list_decks(decks)
            elif command == "create":
                create_new_deck(decks, path)
            elif command == "add":
                add_to_deck(decks, path)
            elif command == "edit":
                edit_a_card(decks, path)
            elif command == "delete":
                delete_something(decks, path)
            elif command == "exit":
                print("Bye! またね！")
                return
            else:
                print(COMMANDS)
    except (EOFError, KeyboardInterrupt):
        # Ctrl+C or Ctrl+Z/Ctrl+D: quit quietly instead of showing an error.
        print()
