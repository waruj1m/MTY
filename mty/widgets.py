from rich.style import Style
from rich.text import Text
from textual.widgets import Static

from mty.words import CHAR_CORRECT, CHAR_CURRENT, CHAR_CURRENT_SPACE, CHAR_EXTRA, CHAR_INCORRECT, CHAR_UNTYPED, STYLE_TEXT


class WordsDisplay(Static):
    """Renders a scrolling, fixed-height window of words with per-char styling."""

    VISIBLE_LINES = 3

    def __init__(self, words: list[str]) -> None:
        super().__init__()
        self.update_words(words)

    def update_words(self, words: list[str]) -> None:
        self.words = words
        self.target = " ".join(words)
        self.word_idx = 0
        self.char_idx = 0
        self.typed: list[list[str]] = [[] for _ in words]

    def render(self) -> Text:
        result = Text(style=Style(color=STYLE_TEXT))
        viewport_width = self.size.width if self.size and self.size.width > 0 else 80
        max_line = viewport_width - 4

        # Lay every word out into wrapped lines, then render only a small
        # window around the current word so the screen stays uncluttered.
        lines = self._wrap_lines(self.words, max_line)
        current_line = next(
            (li for li, indices in enumerate(lines) if self.word_idx in indices), 0
        )
        start = max(0, current_line - 1)
        start = min(start, max(0, len(lines) - self.VISIBLE_LINES))

        for row, word_indices in enumerate(lines[start:start + self.VISIBLE_LINES]):
            if row > 0:
                result.append("\n\n")  # blank row between lines for breathing room
            for pos, wi in enumerate(word_indices):
                if pos > 0:
                    is_current = (wi == self.word_idx and self.char_idx == 0)
                    result.append(
                        " ",
                        style=CHAR_CURRENT_SPACE if is_current else Style(color="#646669"),
                    )
                self._append_word(result, wi)

        return result

    @staticmethod
    def _wrap_lines(words: list[str], max_line: int) -> list[list[int]]:
        """Greedily group word indices into lines that fit the viewport width."""
        lines: list[list[int]] = [[]]
        used = 0
        for wi, word in enumerate(words):
            extra = 1 if lines[-1] else 0
            if lines[-1] and used + extra + len(word) >= max_line:
                lines.append([])
                used = 0
                extra = 0
            lines[-1].append(wi)
            used += extra + len(word)
        return lines

    def _append_word(self, result: Text, wi: int) -> None:
        """Append one word, styling each character against what was typed."""
        word = self.words[wi]
        typed = self.typed[wi]
        for ci in range(max(len(word), len(typed))):
            is_current = (wi == self.word_idx and ci == self.char_idx)
            if ci < len(word):
                target_char = word[ci]
                if is_current:
                    result.append(target_char, style=CHAR_CURRENT)
                elif ci < len(typed):
                    typed_char = typed[ci]
                    style = CHAR_CORRECT if typed_char == target_char else CHAR_INCORRECT
                    result.append(typed_char, style=style)
                else:
                    result.append(target_char, style=CHAR_UNTYPED)
            else:
                if is_current:
                    result.append(" ", style=CHAR_CURRENT)
                elif ci < len(typed):
                    result.append(typed[ci], style=CHAR_EXTRA)
                else:
                    break
