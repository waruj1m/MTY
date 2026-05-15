# mty

A [Monkeytype](https://monkeytype.com)-style typing speed test that runs entirely in your terminal. Built with [Textual](https://textual.textualize.io/).

```
 time  15 30 60 120    words  10 25 50 100
 00:42  |  wpm 78  |  acc 97%  |  raw 81

   the quick brown fox jumps over the lazy

   dog and then some more words appear here

   to keep three lines of text always visible
```

## Install

```bash
pipx install -e .     # recommended — isolated, on your PATH as `mty`
# or
pip install -e .      # into the current environment / virtualenv
```

`mty` requires Python 3.10+. Dependencies (`textual`, `rich`) are installed automatically.

## Usage

```bash
mty                # 30-second timed test (default)
mty --time 60      # timed test: 15, 30, 60, or 120 seconds
mty --words 25     # word-count test: 10, 25, 50, or 100 words
```

The test starts automatically on your first keystroke.

### Keys

| Key | Action |
| --- | --- |
| `1` `2` `3` `4` | Switch to a timed mode (15 / 30 / 60 / 120s) |
| `5` `6` `7` `8` | Switch to a word-count mode (10 / 25 / 50 / 100) |
| `Backspace` | Correct a mistake — works back into previous words |
| `Esc` | End the test early and see results |
| `Enter` / `Tab` | Start a new test (from the results screen) |
| `Ctrl+R` | Reset the current test |
| `Ctrl+Q` | Quit |

Mode keys and the mode bar at the top are clickable; modes can only be
changed before the timer starts.

## Scoring

Following Monkeytype conventions — 1 word counts as 5 characters:

- **wpm** — correctly typed characters ÷ 5 ÷ minutes
- **raw** — every typed character ÷ 5 ÷ minutes (correct or not)
- **acc** — share of characters typed correctly

Correctness is checked per word, so mistyping the length of one word
doesn't throw off the score for everything after it.

## Development

The codebase is small — five modules under `mty/`:

| File | Responsibility |
| --- | --- |
| `app.py` | `MonkeytypeApp` — app state, timing, key handling |
| `widgets.py` | `WordsDisplay` — renders the scrolling 3-line word window |
| `screens.py` | `ResultsScreen` — the end-of-test results modal |
| `stats.py` | `score()` — pure WPM/accuracy scoring |
| `words.py` | Word pool, colour styles, and mode options |

`app.py` is the single source of truth: it mutates `WordsDisplay`'s state
directly, then refreshes it.

Run without installing, and run the tests:

```bash
python -m mty.app                # run from source
pip install -e ".[dev]"          # install with pytest
pytest                           # run the test suite
```
