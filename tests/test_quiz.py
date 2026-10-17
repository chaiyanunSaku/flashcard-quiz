import pytest

from flashcard_quiz.quiz import accepted_answers, check_answer, format_score, shuffled_cards


@pytest.mark.parametrize(
    ("answer", "back"),
    [("a", "a"), (" I ", "i"), ("　a　", "a")],
)
def test_answer_ignores_surrounding_spaces_and_case(answer, back):
    # C1: exact answer, " I " for い (spaces + capital), full-width spaces
    assert check_answer(answer, back)


@pytest.mark.parametrize(
    ("answer", "back"),
    [("ａ", "a"), ("ＴＡＢＥＲＵ", "taberu"), ("ｱ", "ア")],
)
def test_full_width_and_half_width_typing_is_accepted(answer, back):
    # Typed with the Japanese keyboard (IME) on: full-width letters, half-width katakana
    assert check_answer(answer, back)


def test_wrong_answer_is_rejected():
    # C1: "o" for う
    assert not check_answer("o", "u")


def test_empty_answer_is_rejected():
    assert not check_answer("", "u")


def test_any_alternative_is_accepted():
    # C3
    assert check_answer("食べる", "たべる|食べる")
    assert check_answer("たべる", "たべる|食べる")


def test_alternatives_after_edit_are_accepted():
    # C5 (quiz part)
    assert check_answer("みず", "みず|すい")
    assert check_answer("すい", "みず|すい")


def test_spaces_around_bar_are_ignored():
    assert accepted_answers(" みず | すい ") == ["みず", "すい"]
    assert check_answer("すい", "みず | すい")


def test_full_width_bar_separates_alternatives():
    # Card back typed with the Japanese keyboard (IME) on uses "｜" instead of "|"
    assert accepted_answers("日｜び") == ["日", "び"]
    assert check_answer("び", "日｜び")
    assert check_answer("日", "日｜び")


def test_shuffled_cards_uses_given_shuffle_and_keeps_original():
    cards = [{"front": "あ", "back": "a"}, {"front": "い", "back": "i"}]

    result = shuffled_cards(cards, shuffle=lambda order: order.reverse())

    assert result == [{"front": "い", "back": "i"}, {"front": "あ", "back": "a"}]
    assert cards == [{"front": "あ", "back": "a"}, {"front": "い", "back": "i"}]


def test_score_is_correct_over_total():
    # C1: final score
    assert format_score(2, 3) == "2/3"
