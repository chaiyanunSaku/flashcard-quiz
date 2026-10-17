# Checks and decisions

> This file records what I checked, what actually happened, and why I accepted or changed the work. It does not repeat setup instructions or the implementation plan.

## Concrete checks
Write the first two expectations before implementation. Fill in actual results after running them. 

* Cards are written as front → back. The quiz shows the front; the user types the back. `|` separates accepted alternative answers.

| Check / requirement | Given | When | Expected result | Actual result / pass or fail |
|---|---|---|---|---|
| C1 / R2 — normal case | Deck "Hiragana" has 3 cards: あ → a, い → i, う → u | Start a quiz on "Hiragana" and answer "a", " I " (with spaces, capital I), then "o" | First two answers show "Correct!"; the third shows "Wrong" and the correct answer "u". Final score shown is 2/3 | Pass, showed "Correct!" twice, then "Wrong. Answer: u", then "Score: 2/3" (`test_cli.py::test_quiz_marks_answers_and_shows_score`) |
| C2 / R1 — same deck's name creation | Deck "Kanji" already exists | Try to create another deck named "Kanji" | Rejected with a message that the deck already exists; still only one "Kanji" deck in `data/cards.json` | Pass, showed "Deck 'Kanji' already exists!"; still one "Kanji" deck, also with "kanji" (`test_decks.py` duplicate tests) |
| C3 / R2 — alternative answers | Deck "Kanji" has card 食べる → たべる\|食べる | Quiz on "Kanji" and answer "食べる" | Shows "Correct!" | Pass, "食べる" and "たべる" both accepted (`test_quiz.py::test_any_alternative_is_accepted`) |
| C4 / R3 — invalid edit | Deck "Kanji" has card 水 → みず | Edit the card's front or back to "" (empty) | Rejected with "Card cannot be empty!"; the card is still 水 → みず | Pass, empty front and empty back both rejected with "Card cannot be empty!"; card stayed 水 → みず (`test_decks.py::test_edit_to_empty_is_rejected_and_card_unchanged`) |
| C5 / R1, R3 — edit is saved | Deck "Kanji" has card 水 → みず | Edit the back to "みず\|すい", select deck "Kanji" and start | The card is now 水 → みず\|すい, and a quiz accepts either "みず" or "すい" | Pass, card became 水 → みず\|すい and both "みず" and "すい" were accepted (`test_decks.py::test_edit_back_changes_only_back`, `test_quiz.py::test_alternatives_after_edit_are_accepted`) |
| C6 / R3 — cancel delete | Deck "Kanji" exists with 2 cards | Choose delete deck "Kanji" and answer "n" at the confirmation | Deck "Kanji" and both cards are still there | Pass, after "n", showed "Cancelled."; saved file still had "Kanji" with both cards (`test_cli.py::test_answering_n_keeps_the_deck`) |
| C7 / R3 — confirm delete | Deck "Kanji" exists with 2 cards | Choose delete deck "Kanji" and answer "y" at the confirmation | Deck "Kanji" is removed; it no longer appears when choosing a deck to quiz, and it is gone after restarting the app | Pass, after "y", "Kanji" was gone from the saved file and from the `start` deck list after restarting (`test_cli.py::test_answering_y_deletes_the_deck_for_good`) |
| C8 / R2 — empty deck | Deck "Katakana" exists with no cards | Start a quiz on "Katakana" | Shows "This deck has no cards yet." and returns to the menu; the app does not crash | Pass, showed "This deck has no cards yet." and the menu kept running until `exit` (`test_cli.py::test_empty_deck_returns_to_menu`) |


## Two review decisions
- Plan decision: I accepted the AI's plan to keep the deck and answer rules in separate modules from the CLI and to test them with pytest. I changed it by designing the commands myself (`start`, `list`, `create`, `add`, `edit`, `delete`, `exit`), making every deck or card choice a numbered list for consistency, and deciding that deck names are unique ignoring case and that quiz cards are shuffled.
- Code decision: In cli.py, the AI first compared menu answers with plain strip().casefold(), so ｙ typed with the Japanese keyboard on was treated as "no". After finding this in real use, I had it changed so every menu answer goes through one ask() function using the same normalize() as quiz answers, so commands, y/n and numbers all behave the same way.

## Automated tests
- Test file and behaviour checked: `tests/test_storage.py` (decks saved and loaded back, missing file, Japanese kept readable — R1, C7 restart), `tests/test_decks.py` (duplicate deck C2, empty edit rejected C4, edit saved C5, add/delete rules — R1, R3), `tests/test_quiz.py` (spaces/case/full-width spaces C1, `|` alternatives C3 and C5, score `2/3` — R2), `tests/test_cli.py` (full menu runs for C1, C6, C7, C8).
- Command I ran: `uv run pytest -v`
- Final result: 40 passed, 0 failed.
- Correction and rerun, if needed: While using the app, I typed a card's back with the Japanese keyboard on (`日｜び`), and my correct answer "び" was marked wrong because `accepted_answers()` in `quiz.py` only split on the half-width `|`, not the full-width `｜`. I added a test (1 failed, 37 passed), fixed it so `｜` is treated like `|`, and reran: 38 passed (40 after the later fixes).

## Realistic use and final judgment
- Task I tried: Using the Hiragana deck, I added a new card (いよ → 日｜び) with the Japanese keyboard on, changed an existing card with `edit`, and then started a quiz on the deck and answered every card.
- Outcome: Adding and editing worked and were saved to `data/cards.json`. During the quiz my correct answer "び" was marked wrong (`Wrong. Answer: 日｜び`) because the app did not treat the full-width `｜` as a separator, a bug the automated tests had missed. After the fix, I restarted the app and the same card accepted "び". I think I can really use this for my practice.  
- Judgment: Done. R1–R3 work in the app: checks C1–C8 all pass, 40 automated tests pass, and in real use I could add, edit and quiz on my own cards, with the bugs found in real use (full-width `｜` and `ｙ`) fixed and confirmed. A final code review also found that a full-width deck name (`Ｋａｎｊｉ`) slipped past the duplicate check; it is now rejected too.
- Remaining limitation or unfinished work: Commands and y/n answers must be English words. Full-width letters typed with the Japanese keyboard on (like `ｙ` or `ｓｔａｒｔ`) now work, but Japanese words do not, so typing `はじめよ` instead of `start` just shows the command list, and `はい` instead of `y` counts as no. A useful future addition is accepting Japanese words for each command, so learners can stay in Japanese while practising.