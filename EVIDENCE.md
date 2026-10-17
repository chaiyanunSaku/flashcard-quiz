# Checks and decisions

> This file records what I checked, what actually happened, and why I accepted or changed the work. It does not repeat setup instructions or the implementation plan.

## Concrete checks
Write the first two expectations before implementation. Fill in actual results after running them. 

* Cards are written as front → back. The quiz shows the front; the user types the back. `|` separates accepted alternative answers.

| Check / requirement | Given | When | Expected result | Actual result / pass or fail |
|---|---|---|---|---|
| C1 / R2 — normal case | Deck "Hiragana" has 3 cards: あ → a, い → i, う → u | Start a quiz on "Hiragana" and answer "a", " I " (with spaces, capital I), then "o" | First two answers show "Correct!"; the third shows "Wrong" and the correct answer "u". Final score shown is 2/3 | Not run yet |
| C2 / R1 — same deck's name creation | Deck "Kanji" already exists | Try to create another deck named "Kanji" | Rejected with a message that the deck already exists; still only one "Kanji" deck in `data/cards.json` | Not run yet |
| C3 / R2 — alternative answers | Deck "Kanji" has card 食べる → たべる\|食べる | Quiz on "Kanji" and answer "食べる" | Shows "Correct!" | Not run yet |
| C4 / R3 — invalid edit | Deck "Kanji" has card 水 → みず | Edit the card's front or back to "" (empty) | Rejected with "Card cannot be empty!"; the card is still 水 → みず | Not run yet |
| C5 / R1, R3 — edit is saved | Deck "Kanji" has card 水 → みず | Edit the back to "みず\|すい", select deck "Kanji" and start | The card is now 水 → みず\|すい, and a quiz accepts either "みず" or "すい" | Not run yet |
| C6 / R3 — cancel delete | Deck "Kanji" exists with 2 cards | Choose delete deck "Kanji" and answer "n" at the confirmation | Deck "Kanji" and both cards are still there | Not run yet |
| C7 / R3 — confirm delete | Deck "Kanji" exists with 2 cards | Choose delete deck "Kanji" and answer "y" at the confirmation | Deck "Kanji" is removed; it no longer appears when choosing a deck to quiz, and it is gone after restarting the app | Not run yet |
| C8 / R2 — empty deck | Deck "Katakana" exists with no cards | Start a quiz on "Katakana" | Shows "This deck has no cards yet." and returns to the menu; the app does not crash | Not run yet |


## Two review decisions
- Plan decision: I accepted the AI's plan to keep the deck and answer rules in separate modules from the CLI and to test them with pytest. I changed it by designing the commands myself (`start`, `list`, `create`, `add`, `edit`, `delete`, `exit`), making every deck or card choice a numbered list for consistency, and deciding that deck names are unique ignoring case and that quiz cards are shuffled.
- Code decision: [File/function/component, what I accepted or changed, and why. One or two sentences.]

## Automated tests
- Test file and behaviour checked: [...]
- Command I ran: [...]
- Final result: [Actual test count and outcome.]
- Correction and rerun, if needed: [Brief account, or None needed.]

## Realistic use and final judgment
- Task I tried: [One realistic use from start to finish.]
- Outcome: [What happened and whether it served the intended user/purpose.]
- Judgment: [Done / Partly done / Not done, with a brief reason based on the evidence.]
- Remaining limitation or unfinished work: [One specific item, or a useful next check.]