# Implementation plan

> This file records my project-specific steps reviewed before coding. Replace the prompts below with the agreed plan; refer to R1–R3 rather than copying the requirements here.

## Steps
1. **Storage (R1)** — `src/flashcard_quiz/storage.py`: `load_decks(path)` returns `{deck_name: [{"front", "back"}, ...]}` (empty `{}` if the file is missing) and `save_decks(decks, path)` writes UTF-8 JSON with `ensure_ascii=False`. The path is a parameter so tests use a temp folder. Add sample decks in `data/cards.json` (Hiragana, Kanji, and an empty Katakana).
2. **Deck and card logic (R1, R3)** — `src/flashcard_quiz/decks.py`: `create_deck`, `add_card`, `edit_card`, `delete_card`, `delete_deck`. Pure functions with no `input()`/`print()`; a broken rule raises `ValueError` with the message to show, and the CLI prints it. Rules:
   - Deck names are unique ignoring case ("kanji" duplicates "Kanji").
   - Empty front or back (after trimming) is rejected with "Card cannot be empty!".
   - `edit_card` validates before changing anything, so a rejected edit leaves the card unchanged.
3. **Answer checking and score (R2)** — `src/flashcard_quiz/quiz.py`: `normalize(text)` uses `strip()` (also removes full-width spaces) and `casefold()`. `check_answer(answer, back)` splits the back on `|`, trims each alternative, and accepts a match with any of them. `format_score(correct, total)` returns e.g. `2/3`. Card order is shuffled; the shuffle function is passed in so tests can fix the order.
4. **CLI (R1, R2, R3)** — `src/flashcard_quiz/cli.py`, called from `main()` in `__init__.py`. It prints the 勉強しよう！ banner, then the command list, then waits for a command. Whenever the user has to choose a deck or a card, the app prints a numbered list and the user types the number (e.g. `start` → `1` starts the first deck). A number that is not in the list shows "Invalid choice." and returns to the menu.
   - `start`: pick a deck, answer each card's front by typing its back. Show "Correct!" or "Wrong" with all accepted answers, then the final score. An empty deck shows "This deck has no cards yet." and returns to the menu.
   - `list`: show the existing decks with their card counts.
   - `create`: name a new deck, then "Add a card? (y/n)" and loop asking for front and back until "n".
   - `add`: pick an existing deck and add cards with the same loop.
   - `edit`: pick a deck, see a numbered card list, pick a number, then choose `front`/`back`/`both` and type the new text.
   - `delete`: choose `deck` or `card`. For a deck, pick it from a numbered list and confirm "Delete deck 'Kanji'? (y/n)"; only "y" deletes. For a card, pick the deck and the card number; there is no confirmation.
   - `exit`: quit.
   - Unknown commands reprint the command list. Every change is saved with `save_decks` immediately.
5. **Automated tests (`uv run pytest`)**
   - `tests/test_quiz.py`: C1 answer rules and `2/3`, C3, and the quiz part of C5.
   - `tests/test_decks.py`: C2, C4, and the edit part of C5.
   - `tests/test_storage.py`: save and reload, covering R1 persistence and C7's "gone after restart".
   - `tests/test_cli.py`: runs the real menu as if a user were typing. The test gives the app pre-written answers instead of keyboard input (pytest's `monkeypatch`), then checks what was printed on screen (pytest's `capsys`) and what was saved. Covers C1 (cards in a fixed order instead of shuffled), C6, C7, and C8.
6. **Realistic use** — run `uv run flashcard-quiz` as a student would. Create a "Kanji" deck with about 5 cards, including one with `|` alternatives. Quiz on it and score it, fix a card with `edit`, `exit`, restart, and confirm the deck and edit are still there. Then quiz again and delete the deck.

## Later changes, if any
- Tests are written right after each module (storage → `test_storage.py`, decks → `test_decks.py`, and so on) instead of all at once in step 5, so each piece is shown to work before the next one is built on it.
- After real use and review, input typed with the Japanese keyboard on is accepted everywhere (answers, `｜`, menu commands, y/n, deck names), because the app is for Japanese learners.
