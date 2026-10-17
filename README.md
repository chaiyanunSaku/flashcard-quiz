# 勉強しよう！「Let's study!」

## Purpose
[Who will use it, and what will it help them do? One or two sentences.]
Students that want practice Japanese langugage writing system such as Hiragana, Katakana, Kanji, and grammar by using this flashcard CLI.

## Requirements
- R1: The user can create a named deck (e.g. Kanji) and add cards (front and back). Decks and cards are saved to 'data/cards.json' and are still there next time the app runs. Deck name must be unique, and empty fronts or backs are rejected.
- R2: Starting a quiz on a deck with no cards shows "This deck has no cards yet." and returns to the menu instead of crashing. The user picks a deck and is quizzed only on that deck's cards. Answers are accepted if they match ignoring surrounding spaces (including full-width spaces) and letter case. A card's back may list alternatives separated by `|` (e.g. `たべる|食べる`). The score is shown at the end as correct/total (e.g. `8/10`).
- R3: The user can edit a card's front or back, delete a card, or delete a whole deck. Deleting a deck asks for confirmation (y/n) and only deletes on "y". Editing a card to an empty front or back is rejected and the card stays unchanged.

## Setup and use
- Prerequisites: [uv](https://docs.astral.sh/uv/) (it installs Python 3.12+ automatically if needed).
- Setup: Clone the repository by using the following commands.
  git clone https://github.com/chaiyanunSaku/flashcard-quiz.git
  cd flashcard-quiz
  uv sync
- Run: `uv run flashcard-quiz`
  The app shows a 勉強しよう！ banner and a list of commands.
- Run tests: `uv run pytest`

## Author and acknowledgements
- Name / student ID: Chaiyanun Sakulsaowapakkul 6681299
- AI tools used: GitHub Copilot
- External code/resources: None

See PLAN.md for the implementation plan and EVIDENCE.md for results and decisions.