# X3 harder-task band — oracle verification (worker B)

All oracles were verified on disk 2026-10-01: parent worktree + ONLY the
fix commit's test files overlaid -> grading nodes must FAIL; fix worktree
-> same nodes must PASS. Rich ran under a venv with pytest+pygments;
click ran with `PYTHONPATH=<tree>/src` (src layout) and pytest.

Existing band context: rich-u1..u4, nx-t1..t4. Copilot base (Haiku 4.5)
passed every task it ran, so these five target subtler invariants.

---

## rich-u5-split-cells-double-width

- fix: `babf74a7eafb0a989efd88dcfb969cfa2922a58d` ("more tests", 2024-10-04)
- parent: `4f40703e4fa01a749b306b2161a425a314b85606`
- fix diff stat: `rich/segment.py | 6 +++---`, `tests/test_segment.py | 30 ++++---`
- why harder: the `_split_cells` overshoot branch probes the character on
  the wrong side of the cut (`text[pos]` instead of `text[pos-1]`) when the
  cut lands one cell past a double-width char; spotting it requires reading
  the `pos`/`cell_pos` loop invariant, and the obvious-looking
  proportional estimator is a red herring.
- grading nodes: `tests/test_segment.py::test_split_cells_mixed`

oracle at parent (fix's tests/test_segment.py overlaid):

```
E            +  where 21 = cell_len('南無阿弥JKうらめしや ')
E            +    where '南無阿弥JKうらめしや ' = Segment('南無阿弥JKうらめしや ').text

tests/test_segment.py:307: AssertionError
=========================== short test summary info ============================
FAILED tests/test_segment.py::test_split_cells_mixed[segment2] - AssertionErr...
FAILED tests/test_segment.py::test_split_cells_mixed[segment3] - AssertionErr...
2 failed, 3 passed in 0.45s
```

oracle at fix:

```
.....                                                                    [100%]
5 passed in 0.17s
```

## rich-u6-panel-title-background

- fix: `30e5ed61a6064220fe2ff40f4713463488ee6d07` (2025-05-01)
- parent: `69e1618f1f3aae6589cd6210d9d318ab0cdf91da`
- fix diff stat: `rich/panel.py | 7 +++----`, `tests/test_panel.py | 24 +++`
- why harder: the title is stylized with the *border-only* style while the
  panel background lives in the combined style; the symptom (title missing
  `on blue`) points at the title render code, but the fix is in which of
  two nearly identical style variables is passed to `stylize_before`.
- grading nodes: `tests/test_panel.py::test_title_text_with_panel_background`

oracle at parent (fix's tests/test_panel.py overlaid):

```
FAILED tests/test_panel.py::test_title_text_with_panel_background - Assertion...
1 failed, 1 warning in 0.32s
```

oracle at fix:

```
1 passed, 1 warning in 0.26s
```

## rich-u7-wrap-double-width

- fix: `59b1aca63bf9ec69ada93af960d8b2a7bd920477` (2023-11-14, PR #3180)
- parent: `b32e42bda00c6275d4e18dcbe298268094359549`
- fix diff stat: `rich/_wrap.py | 73 ++++---`, `rich/cells.py | 54 ++++---`,
  `tests/test_cells.py | 19 +`, `tests/test_text.py | 66 +`
- why harder: two files change together — `divide_line` mixes character
  counts with cell counts in its fold state machine and `chop_cells` can
  cut inside a double-width glyph and returns pieces in the wrong order;
  the fix is a 177-line rework of the wrap/fold logic, not a local patch.
- grading nodes:
  `tests/test_cells.py::test_chop_cells`,
  `tests/test_cells.py::test_chop_cells_double_width_boundary`,
  `tests/test_cells.py::test_chop_cells_mixed_width`,
  `tests/test_text.py::test_wrap_cjk_mixed`

oracle at parent (fix's test files overlaid):

```
tests/test_text.py:463: AssertionError
=========================== short test summary info ============================
FAILED tests/test_cells.py::test_chop_cells - AssertionError: assert ['kji', ...
FAILED tests/test_cells.py::test_chop_cells_double_width_boundary - Assertion...
FAILED tests/test_cells.py::test_chop_cells_mixed_width - AssertionError: ass...
FAILED tests/test_text.py::test_wrap_cjk_mixed - AssertionError: assert '123...
4 failed, 4 passed in 0.68s
```

oracle at fix:

```
........                                                                 [100%]
8 passed in 1.13s
```

## click-c1-flag-value-optional

- fix: `91de59c6c8abc8251e7af551cd4546cc964288af` (2025-10-07, issue #3084)
- parent: `7f7bbe4569ea68e8dabee232eade069ef3310aea`
- fix diff stat: `src/click/core.py | 13 ++++++---`,
  `tests/test_options.py | 34 ++++`
- why harder: `_flag_needs_value` was derived only from `default is UNSET`,
  ignoring `flag_value`, so the parser demands a value and exits 2; the
  symptom (a usage error at parse time) is far from the one-expression
  site in `Option.__init__`, and the correct condition must thread three
  sentinels (`is_flag`, `flag_value`, `default`).
- grading nodes:
  `tests/test_options.py::test_flag_value_optional_behavior`,
  `tests/test_options.py::test_flag_value_with_type_conversion`

oracle at parent (fix's tests/test_options.py overlaid), with
`PYTHONPATH=<tree>/src`:

```
>       assert result.exit_code == 0
E       assert 2 == 0
E        +  where 2 = <Result SystemExit(2)>.exit_code

tests/test_options.py:2310: AssertionError
=========================== short test summary info ============================
FAILED tests/test_options.py::test_flag_value_optional_behavior - assert 2 == 0
FAILED tests/test_options.py::test_flag_value_with_type_conversion - assert 2...
2 failed in 0.85s
```

oracle at fix:

```
..                                                                       [100%]
2 passed in 0.31s
```

## click-c2-help-option-eagerness

- fix: `70c673d37eb91ba42a129be9037caf3ebed62f3e` (2024-11-30, PR #2811)
- parent: `273fb90106726daa16e1033eca0d677de76345eb`
- fix diff stat: `src/click/core.py | 31 +++++---`,
  `tests/test_commands.py | 132 ++++`
- why harder: `get_help_option` built a fresh `HelpOption` on every call,
  defeating the object-identity comparison that `iter_params_for_processing`
  uses for callback ordering — so `--my-help` loses eagerness only in some
  invocation orders; nothing about the symptom suggests a factory method
  creating duplicate objects.
- grading nodes: `tests/test_commands.py::test_help_param_priority`
  (the companion node `test_iter_params_for_processing` passes at parent
  too — pure sort-logic unit tests — so it is intentionally not graded)

oracle at parent (fix's tests/test_commands.py overlaid), with
`PYTHONPATH=<tree>/src`:

```
        assert "Value of a is: True" not in result.stdout
>       assert "Value of b is: True" not in result.stdout
E       AssertionError: assert 'Value of b is: True' not in 'Value of b is: True\n'

tests/test_commands.py:435: AssertionError
=========================== short test summary info ============================
FAILED tests/test_commands.py::test_help_param_priority - AssertionError: ass...
1 failed, 34 passed in 0.24s
```

oracle at fix:

```
...................................                                      [100%]
35 passed in 0.21s
```

---

## Rejected candidates

- rich `f2ee2953` (infinite loop in Text.append): the oracle test hangs at
  parent instead of failing — ungradeable.
- rich `4f40703e` alone as fix: incomplete — its own test file fails at the
  fix commit for one cut position; superseded by `babf74a7` (used as u5).
- rich `a8c3b870`: same function as u5, smaller change — skipped for
  diversity.
- rich `95fe8ff5`, `16b38304`, `f591471c`, `68e1b638`: one-line/one-char
  fixes, no discriminating mechanism — dropped per the one-line rule.
- rich `2d7a94d7` (broken pipe): oracle test is subprocess-based and flaky
  in a sandbox — dropped.
- rich `9175392a`, `0ab24672`: new features (env vars), not bug fixes.
- rich `5daf203d`, `655b5210`: refactors, no behavior fix.
- click `9caedb92` (envvar/flag reconciliation): large, famous PR;
  considered, but `70c673d3` chosen as the less-famous, subtler-identity
  candidate.
- click `955ca492`, `17874977`, `1a4d8c1b`: too small / adjacent to chosen
  commits.
- click `0ef55fda`, `43a7d70f`, `4ece17a1`: feature-ish or heavier than the
  two chosen; only two click slots.
