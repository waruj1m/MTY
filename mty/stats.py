"""Pure typing-test scoring — no Textual, no app state, easy to test."""


def score(
    words: list[str],
    typed: list[list[str]],
    word_idx: int,
    elapsed: float,
) -> dict:
    """Score a typing test from its raw state.

    Each word's typed characters are compared against *its own* target word
    (rather than one flattened string), so a wrong-length word cannot shift
    every later character out of alignment.

    Monkeytype conventions: 1 word == 5 characters; the space after a
    completed word counts as a correct character; ``wpm`` counts only
    correct characters while ``raw`` counts everything typed.

    Args:
        words: the target words.
        typed: per-word lists of characters the user has entered.
        word_idx: index of the word currently being typed.
        elapsed: seconds since the test started.
    """
    correct = incorrect = extra = missed = 0
    for wi in range(word_idx + 1):
        target = words[wi]
        entered = typed[wi]
        for ci, ch in enumerate(entered):
            if ci < len(target):
                if ch == target[ci]:
                    correct += 1
                else:
                    incorrect += 1
            else:
                extra += 1
        if wi < word_idx:  # a completed word
            missed += max(0, len(target) - len(entered))
            correct += 1  # the space separating it from the next word

    total = correct + incorrect + extra
    # WPM measured over a sub-second window is just noise — clamp the
    # denominator to 1s so the live stat bar can't spike on the first
    # keystroke. Real tests run far longer, so final scores are unaffected.
    minutes = max(elapsed, 1.0) / 60
    return {
        "wpm": (correct / 5) / minutes,
        "raw": (total / 5) / minutes,
        "accuracy": (correct / total * 100) if total > 0 else 100.0,
        "time": elapsed,
        "correct": correct,
        "incorrect": incorrect,
        "extra": extra,
        "missed": missed,
    }
