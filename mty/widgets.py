from rich.style import Style
from rich.text import Text
from textual.widgets import Static

from mty.words import CHAR_CORRECT, CHAR_CURRENT, CHAR_CURRENT_SPACE, CHAR_EXTRA, CHAR_INCORRECT, CHAR_UNTYPED, STYLE_TEXT


class WordsDisplay(Static):
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
        line_used = 0

        for wi, word in enumerate(self.words):
            if wi > 0:
                extra = 1
                if line_used + len(word) + extra >= max_line:
                    result.append("\n")
                    line_used = 0
                if line_used > 0:
                    space_pos = wi - 1
                    is_current = (wi == self.word_idx and self.char_idx == 0)
                    if is_current:
                        result.append(" ", style=CHAR_CURRENT_SPACE)
                    else:
                        result.append(" ", style=Style(color="#646669"))
                    line_used += 1

            wc = self.typed[wi]
            for ci in range(max(len(word), len(wc))):
                is_current = (wi == self.word_idx and ci == self.char_idx)
                if ci < len(word):
                    target_char = word[ci]
                    if is_current:
                        result.append(target_char, style=CHAR_CURRENT)
                    elif ci < len(wc):
                        typed = wc[ci]
                        if typed == target_char:
                            result.append(typed, style=CHAR_CORRECT)
                        else:
                            result.append(typed, style=CHAR_INCORRECT)
                    else:
                        result.append(target_char, style=CHAR_UNTYPED)
                else:
                    if is_current:
                        result.append(" ", style=CHAR_CURRENT)
                    elif ci < len(wc):
                        result.append(wc[ci], style=CHAR_EXTRA)
                    else:
                        break
                line_used += 1

        return result
