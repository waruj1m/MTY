# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

`mty` — a Monkeytype-style typing speed test that runs entirely in the terminal, built on [Textual](https://textual.textualize.io/).

## Commands

```bash
pip install -e .          # install (editable) with deps: textual, rich
mty                       # run — defaults to 30s timed test
mty --time 60             # timed mode (choices: 15, 30, 60, 120)
mty --words 25            # word-count mode (choices: 10, 25, 50, 100)
python -m mty.app         # run without installing
```

No test suite, linter, or build step is configured. `requires-python >= 3.10`.

## Architecture

Single-process Textual app, 4 modules under `mty/`:

- **`app.py`** — `MonkeytypeApp` owns all state and game logic: the timer
  (`set_interval(0.1, self._tick)`), the active mode, and the word list. **All
  keystrokes are handled in `App.on_key`**, not by a focused input widget — typed
  characters are pushed into `WordsDisplay.typed`, and the test auto-starts on the
  first keystroke. The CSS theme (Monkeytype's dark palette) lives inline in
  `MonkeytypeApp.CSS`.
- **`widgets.py`** — `WordsDisplay` is a pure-render `Static`. It owns no game
  logic; `app.py` mutates its `typed` / `word_idx` / `char_idx` fields directly,
  then calls `.refresh()`. `render()` rebuilds a Rich `Text` each frame: it
  word-wraps all words (`_wrap_lines`), then renders only a `VISIBLE_LINES`-tall
  (3) window centered on the current line, with per-character coloring.
- **`screens.py`** — `ResultsScreen`, a `ModalScreen` shown on test completion.
- **`words.py`** — word pool (`WORDS`, deduped) plus Rich `Style` constants and
  the `TIME_OPTIONS` / `WORD_OPTIONS` lists. Style/color changes go here.

### Key conventions

- **State flow:** `app.py` is the single source of truth. `WordsDisplay` is a dumb
  view — never add game logic to it; mutate its fields from `app.py` and `refresh()`.
- **WPM/accuracy** are computed by `_compute_stats()`, the single source for
  both the live stats bar and the final results. It compares `typed` vs.
  `target` **word by word** (not as a flattened string) so a wrong-length word
  cannot misalign every later character. 5 chars == 1 word; `wpm` counts only
  correct chars, `raw` counts everything typed.
- **Mode switching** (digit keys `1`-`8`, or clicking the mode bar) regenerates the
  word list and resets all counters; it is blocked once the timer is running.
- Timed mode pre-generates 200 words; word mode generates `count + 10`.

<!-- cce-block-version: 3 -->
## Context Engine (CCE)

This project uses Code Context Engine for intelligent code retrieval and
cross-session memory.

### Searching the codebase

**You MUST use `context_search` instead of reading files directly** when
exploring the codebase, answering questions about code, or understanding how
things work. This is a hard requirement, not a suggestion. `context_search`
returns the most relevant code chunks with confidence scores instead of whole
files, and tracks token savings automatically.

When to use `context_search`:
- Answering questions about the codebase ("how does X work?", "where is Y?")
- Exploring structure or architecture
- Finding related code, functions, or patterns
- Any time you would otherwise read a file just to understand it

When to use `Read` instead:
- You need to edit a specific file (read before editing)
- You need the exact, complete content of a known file path

Other search tools:
- `expand_chunk` — get full source for a compressed result
- `related_context` — find what calls/imports a function

### Cross-session memory — use it actively

This project has persistent memory across Claude Code sessions. **You must
use it both ways: recall before answering, record after deciding.** Memory
that is not recorded is lost; memory that is not recalled does nothing.

**Before answering a non-trivial question, call `session_recall`.**
Especially when:
- The question touches architecture, design, or naming choices
- The user asks "what / why / how did we ..."
- You are about to recommend an approach the team may have already chosen
  or already rejected

Pass a topic phrase, not a single word — e.g. `session_recall("auth flow")`,
not `session_recall("auth")`. Recall is vector-similarity-based, so paraphrases
match. If recall returns relevant entries, lead with them ("Per a prior
decision: ...") instead of re-deriving the answer.

**After making a non-obvious decision, call `record_decision`.** Especially:
- Choosing one library / pattern / approach over another
- Resolving an ambiguity in the spec or requirements
- Establishing a convention the project should follow going forward
- Anything you would not want to re-litigate next session

Format: `record_decision(decision="...", reason="...")`. Keep both fields
short and specific — they are surfaced verbatim at the start of future
sessions.

**After meaningful work in a file, call `record_code_area`.** Especially when:
- You added or substantially modified a function/class
- You traced through a non-obvious flow and want future-you to find it fast

Format: `record_code_area(file_path="...", description="...")`.

Skip recording for trivial reads, formatting changes, or one-off lookups —
the goal is durable signal, not an event log.

### Drilling deeper from a recall hit

`session_recall` results are tagged with the source session id, e.g.
`[turn sid:abc123|n:5]`. To drill in:

- `session_timeline(session_id="abc123")` — walk the per-turn summaries of
  that session in order. Use this when the user asks "what was the
  reasoning?" or "how did we get there?".
- `session_event(event_id=N)` — fetch a specific tool event's raw input
  and output (capped at 4 KB at read time). Use this when a turn summary
  references a tool result you actually need to inspect.

Both are read-only and cheap. Prefer them over re-running tool calls or
asking the user to re-paste context.

## Output Style

Be concise. Lead with the answer or action, not reasoning. Skip filler words,
preamble, and phrases like "I'll help you with that" or "Certainly!". Prefer
fragments over full sentences in explanations. No trailing summaries of what
you just did. One sentence if it fits.

Code blocks, file paths, commands, and error messages are always written in full.
<!-- /cce-block -->
