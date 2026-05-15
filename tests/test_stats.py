import pytest

from mty.stats import score


def test_perfect_run():
    words = ["the", "quick", "brown"]
    typed = [list("the"), list("quick"), list("brown")]
    s = score(words, typed, word_idx=2, elapsed=60.0)
    # 3 + 5 + 5 letters, plus 2 spaces after the two completed words = 15
    assert s["correct"] == 15
    assert s["incorrect"] == 0
    assert s["extra"] == 0
    assert s["missed"] == 0
    assert s["wpm"] == 3.0  # 15 chars / 5 over 1 minute
    assert s["raw"] == 3.0
    assert s["accuracy"] == 100.0


def test_wrong_length_word_does_not_misalign_later_words():
    # The original bug: an extra letter shifted every later character.
    words = ["cat", "dog", "fish"]
    typed = [list("cat"), list("dogs"), list("fish")]  # extra 's' on word 1
    s = score(words, typed, word_idx=2, elapsed=60.0)
    # word 0: 3 correct + space; word 1: 3 correct + 1 extra + space;
    # word 2 (current): 4 correct  ->  still scored correctly despite the extra
    assert s["correct"] == 3 + 1 + 3 + 1 + 4
    assert s["extra"] == 1
    assert s["incorrect"] == 0


def test_incorrect_characters():
    words = ["the"]
    typed = [list("teh")]  # t ok, e!=h, h!=e
    s = score(words, typed, word_idx=0, elapsed=60.0)
    assert s["correct"] == 1
    assert s["incorrect"] == 2
    assert s["accuracy"] == pytest.approx(100 / 3)


def test_missed_characters_on_a_skipped_word():
    words = ["hello", "world"]
    typed = [list("hel"), list("wo")]  # advanced past "hello" early
    s = score(words, typed, word_idx=1, elapsed=60.0)
    assert s["missed"] == 2
    assert s["correct"] == 3 + 1 + 2  # 3 letters + space + 2 on current word


def test_early_keystroke_wpm_is_clamped():
    # elapsed ~0 must not blow wpm up to thousands.
    words = ["the", "quick"]
    typed = [list("t"), []]
    s = score(words, typed, word_idx=0, elapsed=0.001)
    assert s["wpm"] <= 12.0  # denominator clamped to a 1-second window


def test_no_input_is_safe():
    words = ["the", "quick"]
    typed = [[], []]
    s = score(words, typed, word_idx=0, elapsed=5.0)
    assert s["wpm"] == 0.0
    assert s["raw"] == 0.0
    assert s["accuracy"] == 100.0
