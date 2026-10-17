# Instructions for this repository

> This file tells the coding agent how to work on this project. It does not replace the requirements or plan.

- Read README.md, PLAN.md and the checks in EVIDENCE.md before implementing.
- Keep changes within the three requirements in README.md.
- Use Python 3.12+ managed with uv. Add packages with `uv add` (never `pip install`), and ask before adding any new dependency.
- App code goes in `src/flashcard_quiz/`, tests in `tests/`, sample data in `data/cards.json`.
- Keep the code modular: logic functions return results and never use `input()` or `print()`; only the CLI code talks to the user.
- Work in small steps: one feature or fix at a time, then stop so the student can review, run and commit it.
- Run the app with: `uv run flashcard-quiz`
- Run tests with: `uv run pytest`
- If the instruction were not clear or you have questions then ask before moving on.
- Do not implement yet until I say so.
- Do not change an expected result merely to make a test pass. Raise any disagreement for review.
- Leave requirements, expected results, decision notes and the final judgment for the student to write.