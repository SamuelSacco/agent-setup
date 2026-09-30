# RUN rich-u1-pretty-dataclass-unset-field — claude / orient

Date: 2026-09-30. Produced by `scripts/run-eval.sh` (packaged eval runner).

**VERDICT: PASS — grading tests pass on disk (1/1 nodes).**

Claim under test: The base tool, given only the symptom report, produces a library fix that passes the real fix commit's grading tests on disk.

| Field | Value |
|---|---|
| Task | rich-u1-pretty-dataclass-unset-field — Rich: pretty-printing a dataclass with an unset field crashes |
| Tool / arm | claude / orient |
| Model | opus |
| Success (disk-graded) | yes |
| Turns | 5 |
| Cost USD | 0.1087 — metered (tool JSON envelope) |
| Wall s | 52 |
| Grading python | /home/hatch/workspace/p2/secondcode/venv/bin/python (explicit (--python / EVAL_PYTHON)) |
| Source clone | /home/hatch/workspace/p2/secondcode/.infra/rich-src (parent b6f2f7aa5, fix 6055e2d8e) |
| Run dir | /home/hatch/workspace/p3/bigmodel/evals/scratch-run-eval/runs/rich-u1-pretty-dataclass-unset-field-claude-orient-20260930-185523 |
| Diff stat (excl. setup + grading tests) |  1 file changed, 3 insertions(+), 1 deletion(-) |
| Pytest tail | .                                                                                                                                                                                                [100%] | 1 passed in 0.28s |

Agent's own summary (self-report — not the grade):

```
The crash is fixed. An unset field is now left out, so `BadDataclass()` prints as `BadDataclass()`, and dataclasses with all fields set print the same as before.

**Root cause:** When rendering a dataclass, `_traverse` in `rich/pretty.py` loops over the fields that have `field.repr` set and calls `getattr(obj, field.name)` on each one. A field declared with `field(init=False)` and no default never becomes an attribute on the instance, so that `getattr` raised `AttributeError`.

**Change:** In `rich/pretty.py`, the loop that builds the fields to show now also requires `hasattr(obj, field.name)`, so unset fields are skipped. Because the filter runs before `loop_last`, the last field shown still gets the right trailing-comma and layout handling. If no fields are left, the node falls back to its existing empty form, `ClassName()`.

**Verification:**
- The reported case prints `BadDataclass()` through both `pretty_repr` and `Console().print`.
- A mixed case with an unset field between two set ones prints `Mixed(a=1, b=2)`.
- `/home/hatch/workspace/p2/secondcode/venv/bin/python -m pytest tests/test_pretty.py -q`: 50 passed, 1 skipped.
```
