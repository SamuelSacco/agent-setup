# Rich — orientation

Rich is a Python library for rich text and terminal formatting:
styles, tables, panels, markdown, syntax highlighting, progress bars.
Package code lives in `rich/` as mostly flat modules; import it as
`import rich` / `from rich.console import Console`.

## Layout

- `rich/console.py` — the `Console` class: printing, capture/export,
  the render pipeline. Everything printable flows through here.
- `rich/text.py` — `Text`, the styled-text workhorse (spans, wrapping,
  justification). `rich/segment.py` — `Segment`, the atomic
  (text, style, control) unit every renderable ultimately produces.
- `rich/cells.py` — terminal cell-width measurement (`cell_len`,
  `get_character_cell_size`), with cached width tables in
  `rich/_unicode_data/`. Width bugs live here or in segment splitting.
- `rich/style.py`, `rich/color.py` — style parsing/rendering and the
  color systems (standard/256/truecolor downgrade chain).
- Renderables: `rich/table.py`, `rich/panel.py`, `rich/columns.py`,
  `rich/markdown.py` (markdown-it-py based), `rich/syntax.py`
  (Pygments), `rich/pretty.py` (pretty-printing of arbitrary objects,
  `pretty_repr` / `traverse`), `rich/tree.py`, `rich/progress.py`.
- Tests live in the top-level `tests/` directory, one `test_<module>.py`
  per module (e.g. `tests/test_table.py` for `rich/table.py`).

## Conventions

- Renderables implement `__rich_console__(console, options)` yielding
  `Segment`s, and usually `__rich_measure__` for min/max widths.
  Rendering options (width, justify, style) travel in
  `ConsoleOptions`; never read terminal size directly inside a
  renderable.
- Text is measured in *cells*, not characters: wide (CJK) characters
  take 2 cells, combining/zero-width characters 0. Splitting and
  wrapping must happen on cell boundaries via `Segment` helpers, never
  by slicing the raw string.
- Styles are immutable value objects (`Style.parse("bold red on
  white")`); combine with `+`, resolve to ANSI via the console's color
  system. Output for a given style must be identical in capture/record
  and live modes.
- User-facing errors use exceptions from the module or
  `rich.errors`; don't print from library code except through a
  `Console`.
- Match the local style of the file you are editing; docstrings are
  Google-style and public APIs are type-annotated.

## Working

- Run tests targeted, never the whole suite, from the repo root:
  `/home/hatch/workspace/p2/secondcode/venv/bin/python -m pytest tests/<file> -q`.
  That interpreter has pytest, Pygments, and markdown-it-py installed.
- Most rendering tests build a `Console` with an explicit width and
  `force_terminal=True` and compare captured output byte-for-byte
  (ANSI escapes included) — reproduce with the same construction when
  a rendered string looks wrong.
- A failing test in `tests/` for the module you are changing is the
  first thing to explain; a green targeted file is the minimum bar
  before you call a fix done.
