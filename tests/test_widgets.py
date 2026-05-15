from mty.widgets import WordsDisplay


def test_wrap_lines_keeps_each_line_within_width():
    words = ["aaa", "bbb", "ccc", "ddd"]
    lines = WordsDisplay._wrap_lines(words, max_line=8)
    for line in lines:
        rendered = " ".join(words[i] for i in line)
        assert len(rendered) <= 8


def test_wrap_lines_covers_every_word_once_in_order():
    words = ["aaa", "bbb", "ccc", "ddd", "eee"]
    lines = WordsDisplay._wrap_lines(words, max_line=8)
    flattened = [i for line in lines for i in line]
    assert flattened == [0, 1, 2, 3, 4]


def test_wrap_lines_single_line_when_width_is_ample():
    words = ["a", "b", "c"]
    lines = WordsDisplay._wrap_lines(words, max_line=100)
    assert lines == [[0, 1, 2]]
