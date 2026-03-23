from logic_utils import check_guess, parse_guess, update_score, get_range_for_difficulty


# --- check_guess tests ---

def test_winning_guess():
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"

def test_hint_message_correct_on_win():
    _, message = check_guess(50, 50)
    assert "Correct" in message

def test_hint_message_says_lower_when_too_high():
    _, message = check_guess(60, 50)
    assert "LOWER" in message

def test_hint_message_says_higher_when_too_low():
    _, message = check_guess(40, 50)
    assert "HIGHER" in message


# --- parse_guess tests ---

def test_parse_valid_int():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None

def test_parse_float_truncates():
    ok, value, err = parse_guess("7.9")
    assert ok is True
    assert value == 7

def test_parse_empty_string():
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None

def test_parse_none():
    ok, value, err = parse_guess(None)
    assert ok is False

def test_parse_non_numeric():
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert "not a number" in err.lower()


# --- update_score tests ---

def test_score_win_first_attempt():
    score = update_score(0, "Win", 1)
    assert score == 90  # 100 - 10*1

def test_score_win_later_attempt():
    score = update_score(0, "Win", 5)
    assert score == 50  # 100 - 10*5

def test_score_win_minimum_10():
    score = update_score(0, "Win", 20)
    assert score == 10  # clamped to 10

def test_score_wrong_guess_loses_5():
    score = update_score(100, "Too High", 1)
    assert score == 95

def test_score_too_low_loses_5():
    score = update_score(100, "Too Low", 1)
    assert score == 95


# --- get_range_for_difficulty tests ---

def test_easy_range():
    assert get_range_for_difficulty("Easy") == (1, 20)

def test_normal_range():
    assert get_range_for_difficulty("Normal") == (1, 100)

def test_hard_range():
    assert get_range_for_difficulty("Hard") == (1, 200)

def test_unknown_difficulty_defaults():
    assert get_range_for_difficulty("Unknown") == (1, 100)
