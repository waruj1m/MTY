from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Label


class ResultsScreen(ModalScreen):
    def __init__(self, stats: dict) -> None:
        super().__init__()
        self.stats = stats

    def compose(self) -> ComposeResult:
        s = self.stats
        with Vertical(classes="results-box"):
            yield Label("test complete", classes="results-title")
            yield Label("", classes="results-spacer")
            with Horizontal(classes="results-stats"):
                with Vertical(classes="results-stat"):
                    yield Label(str(round(s["wpm"])), classes="results-value")
                    yield Label("wpm", classes="results-label")
                with Vertical(classes="results-stat"):
                    yield Label(f"{s['accuracy']:.1f}%", classes="results-value")
                    yield Label("acc", classes="results-label")
                with Vertical(classes="results-stat"):
                    yield Label(str(round(s["raw"])), classes="results-value")
                    yield Label("raw", classes="results-label")
                with Vertical(classes="results-stat"):
                    yield Label(f"{s['time']}s", classes="results-value")
                    yield Label("time", classes="results-label")
            yield Label("", classes="results-spacer")
            with Horizontal(classes="results-detail"):
                yield Label(f"correct: {s['correct_chars']}", classes="results-detail-item")
                yield Label(f"incorrect: {s['incorrect_chars']}", classes="results-detail-item")
                yield Label(f"extra: {s['extra_chars']}", classes="results-detail-item")
                yield Label(f"missed: {s['missed_chars']}", classes="results-detail-item")
            yield Label("", classes="results-spacer")
            yield Label("enter / tab - new test  |  ctrl+q - quit", classes="results-hint")

    BINDINGS = [
        Binding("enter", "dismiss(None)", "new test"),
        Binding("tab", "dismiss(None)", "new test"),
        Binding("escape", "dismiss(None)", "close"),
        Binding("ctrl+q", "quit", "quit", priority=True),
    ]
