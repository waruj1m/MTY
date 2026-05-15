import argparse
import random
import time
from typing import ClassVar, Optional

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.events import Key
from textual.widgets import Footer, Label

from mty.screens import ResultsScreen
from mty.widgets import WordsDisplay
from mty.words import STYLE_BG, TIME_OPTIONS, WORD_OPTIONS, WORDS


class MonkeytypeApp(App):
    TITLE = "mty"
    CSS = """
    Screen { background: #2c2e31; }
    WordsDisplay {
        width: 100%; height: auto; min-height: 6;
        padding: 1 2; background: #2c2e31;
    }
    #mode-bar {
        height: 3; padding: 0 2; background: #2c2e31;
    }
    #mode-bar Label {
        padding: 0 1; color: #646669; background: #2c2e31;
    }
    #mode-bar .active { color: #e2b714; text-style: bold; }
    #mode-bar .sep { color: #2c2e31; width: 1; }
    #stats-bar {
        height: 3; padding: 0 2; background: #2c2e31;
    }
    #stats-bar Label { padding: 0 1; background: #2c2e31; }
    #stats-bar .val { color: #d1d0c5; }
    #stats-bar .lbl { color: #646669; }
    #stats-bar .sep { color: #2c2e31; width: 1; }
    Footer { background: #2c2e31; color: #646669; }
    ResultsScreen { align: center middle; background: rgba(0,0,0,0.6); }
    .results-box { width: 50; height: auto; padding: 2 3; background: #2c2e31; border: tall #e2b714; align: center middle; }
    .results-title { color: #e2b714; text-style: bold; content-align: center middle; height: 3; }
    .results-spacer { height: 1; }
    .results-stats { height: 5; align: center middle; }
    .results-stat { min-width: 10; height: 5; align: center middle; }
    .results-value { color: #d1d0c5; text-style: bold; content-align: center middle; height: 3; }
    .results-label { color: #646669; content-align: center middle; height: 1; }
    .results-detail { height: 3; align: center middle; }
    .results-detail-item { color: #646669; padding: 0 1; }
    .results-hint { color: #646669; content-align: center middle; height: 1; }
    """

    BINDINGS: ClassVar = [
        Binding("ctrl+r", "reset", "reset"),
        Binding("ctrl+q", "quit", "quit", priority=True),
    ]

    def __init__(self, mode: str = "time", value: int = 30) -> None:
        super().__init__()
        self.mode = mode
        self.mode_value = value
        self.timer_running = False
        self.elapsed = 0.0
        self.start_time: Optional[float] = None
        self.finished = False
        self.word_list: list[str] = []
        self._generate_words()

    def _generate_words(self) -> None:
        n = 200 if self.mode == "time" else self.mode_value + 10
        self.word_list = [random.choice(WORDS) for _ in range(n)]
        self.finished = False

    def compose(self) -> ComposeResult:
        with Vertical():
            with Horizontal(id="mode-bar"):
                yield Label(" time ", classes="lbl")
                for t in TIME_OPTIONS:
                    cls = "active" if self.mode == "time" and self.mode_value == t else "lbl"
                    yield Label(f"{t}", id=f"time-{t}", classes=f"mode-click {cls}")
                yield Label("  ", classes="sep")
                yield Label(" words ", classes="lbl")
                for w in WORD_OPTIONS:
                    cls = "active" if self.mode == "words" and self.mode_value == w else "lbl"
                    yield Label(f"{w}", id=f"words-{w}", classes=f"mode-click {cls}")
            with Horizontal(id="stats-bar"):
                yield Label("00:00", id="stat-timer", classes="val")
                yield Label("  |  ", classes="sep")
                yield Label("wpm ", classes="lbl")
                yield Label("0", id="stat-wpm", classes="val")
                yield Label("  |  ", classes="sep")
                yield Label("acc ", classes="lbl")
                yield Label("100%", id="stat-acc", classes="val")
                yield Label("  |  ", classes="sep")
                yield Label("raw ", classes="lbl")
                yield Label("0", id="stat-raw", classes="val")
            self.word_display = WordsDisplay(self.word_list)
            yield self.word_display
            yield Footer()

    def _tick(self) -> None:
        if self.timer_running and self.start_time:
            self.elapsed = time.time() - self.start_time
            if self.mode == "time" and self.elapsed >= self.mode_value:
                self._finish()
                return
            self._update_stats()

    def on_mount(self) -> None:
        self.set_interval(0.1, self._tick)

    def _compute_stats(self) -> dict:
        """Compare typed vs. target word by word.

        Comparing each word against its own target (instead of flattening
        everything into one string) keeps a wrong-length word from shifting
        every later character out of alignment — the bug that made wpm
        collapse to near zero while raw stayed high.

        Monkeytype convention: 1 word == 5 characters, the space after a
        completed word counts as a correct character, wpm counts only
        correct characters, raw counts everything typed.
        """
        dw = self.word_display
        correct = incorrect = extra = missed = 0
        for wi in range(dw.word_idx + 1):
            target = dw.words[wi]
            typed = dw.typed[wi]
            for ci, ch in enumerate(typed):
                if ci < len(target):
                    if ch == target[ci]:
                        correct += 1
                    else:
                        incorrect += 1
                else:
                    extra += 1
            if wi < dw.word_idx:  # a completed word
                missed += max(0, len(target) - len(typed))
                correct += 1  # the space separating it from the next word

        total = correct + incorrect + extra
        e = self.elapsed if self.elapsed > 0 else 0.001
        minutes = e / 60
        return {
            "wpm": (correct / 5) / minutes,
            "raw": (total / 5) / minutes,
            "accuracy": (correct / total * 100) if total > 0 else 100.0,
            "time": e,
            "correct": correct, "incorrect": incorrect,
            "extra": extra, "missed": missed,
        }

    def _update_stats(self) -> None:
        e = self.elapsed if self.elapsed > 0 else 0.001
        if self.mode == "time":
            r = max(0, self.mode_value - e)
            t = f"{int(r // 60):02d}:{int(r % 60):02d}"
        else:
            t = f"{e:.1f}s"

        s = self._compute_stats()
        self.query_one("#stat-timer").update(t)
        self.query_one("#stat-wpm").update(str(round(s["wpm"])))
        self.query_one("#stat-acc").update(f"{s['accuracy']:.0f}%")
        self.query_one("#stat-raw").update(str(round(s["raw"])))

    def _finish(self) -> None:
        if self.finished:
            return
        self.finished = True
        self.timer_running = False
        s = self._compute_stats()
        self.push_screen(ResultsScreen({
            "wpm": s["wpm"], "raw": s["raw"], "accuracy": s["accuracy"],
            "time": round(s["time"]),
            "correct_chars": s["correct"], "incorrect_chars": s["incorrect"],
            "extra_chars": s["extra"], "missed_chars": s["missed"],
        }))

    def _switch_mode(self, mode: str, value: int) -> None:
        self.mode = mode
        self.mode_value = value
        self._generate_words()
        self.elapsed = 0.0
        self.timer_running = False
        self.start_time = None
        self.finished = False
        self.word_display.update_words(self.word_list)
        self.word_display.refresh()
        self.query_one("#stat-timer").update("00:00" if mode == "time" else "0.0")
        self.query_one("#stat-wpm").update("0")
        self.query_one("#stat-acc").update("100%")
        self.query_one("#stat-raw").update("0")
        self._refresh_modes()

    def _refresh_modes(self) -> None:
        for t in TIME_OPTIONS:
            w = self.query_one(f"#time-{t}")
            w.set_class(self.mode == "time" and self.mode_value == t, "active")
            w.set_class(not (self.mode == "time" and self.mode_value == t), "lbl")
        for wc in WORD_OPTIONS:
            w = self.query_one(f"#words-{wc}")
            w.set_class(self.mode == "words" and self.mode_value == wc, "active")
            w.set_class(not (self.mode == "words" and self.mode_value == wc), "lbl")

    def on_key(self, event: Key) -> None:
        if self.finished:
            if event.key in ("enter", "tab", "escape"):
                self.action_reset()
                event.stop()
            return

        if event.key == "ctrl+r":
            self.action_reset()
            event.stop()
            return

        dw = self.word_display

        # Corrections are handled by key name, *before* character input.
        # A backspace can arrive carrying a non-printable character payload
        # (DEL / ^H); checking the key here keeps it from being appended as
        # typed text instead of deleting.
        if event.key in ("backspace", "ctrl+h"):
            if dw.char_idx > 0 and dw.typed[dw.word_idx]:
                dw.typed[dw.word_idx].pop()
                dw.char_idx -= 1
            elif dw.word_idx > 0 and dw.char_idx == 0:
                dw.word_idx -= 1
                dw.char_idx = len(dw.typed[dw.word_idx])
            dw.refresh()
            self._update_stats()
            event.stop()
            return

        if event.key == "escape":
            self._finish()
            event.stop()
            return

        # From here on, only genuine printable characters count as typing.
        ch = event.character
        if ch is None or len(ch) != 1 or not ch.isprintable():
            return

        if not self.timer_running and ch in "12345678":
            mode_map = {"1": ("time", 15), "2": ("time", 30), "3": ("time", 60), "4": ("time", 120),
                        "5": ("words", 10), "6": ("words", 25), "7": ("words", 50), "8": ("words", 100)}
            self._switch_mode(*mode_map[ch])
            event.stop()
            return

        if not self.timer_running:
            self.timer_running = True
            self.start_time = time.time()
            self.elapsed = 0.0

        if ch == " ":
            if dw.char_idx > 0 or dw.typed[dw.word_idx]:
                if dw.word_idx < len(dw.words) - 1:
                    dw.word_idx += 1
                    dw.char_idx = 0
                else:
                    self._finish()
        else:
            dw.typed[dw.word_idx].append(ch)
            dw.char_idx += 1

        dw.refresh()

        if self.mode == "words" and dw.word_idx >= self.mode_value:
            self._finish()

        self._update_stats()

    def action_reset(self) -> None:
        self._generate_words()
        self.elapsed = 0.0
        self.timer_running = False
        self.start_time = None
        self.finished = False
        self.word_display.update_words(self.word_list)
        self.word_display.refresh()
        self.query_one("#stat-timer").update("00:00" if self.mode == "time" else "0.0")
        self.query_one("#stat-wpm").update("0")
        self.query_one("#stat-acc").update("100%")
        self.query_one("#stat-raw").update("0")

    def on_click(self, event) -> None:
        w = event.widget
        if not hasattr(w, 'id'):
            return
        wid = w.id or ""
        if wid.startswith("time-"):
            try:
                v = int(wid.split("-")[1])
                self._switch_mode("time", v)
            except (ValueError, IndexError):
                pass
        elif wid.startswith("words-"):
            try:
                v = int(wid.split("-")[1])
                self._switch_mode("words", v)
            except (ValueError, IndexError):
                pass

    def on_screen_resume(self, event) -> None:
        if self.finished:
            self.action_reset()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="monkeytype-like typing speed test for the terminal",
        epilog="keys: 1-4 time modes, 5-8 word modes, ctrl+r reset, ctrl+q quit",
    )
    parser.add_argument("--time", type=int, choices=TIME_OPTIONS, help="timed test in seconds")
    parser.add_argument("--words", type=int, choices=WORD_OPTIONS, help="word count test")
    a = parser.parse_args()
    mode, value = "time", 30
    if a.words:
        mode, value = "words", a.words
    elif a.time:
        mode, value = "time", a.time
    MonkeytypeApp(mode=mode, value=value).run()


if __name__ == "__main__":
    main()
