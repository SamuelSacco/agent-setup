# RUN rich-u1-pretty-dataclass-unset-field — claude / base

Date: 2026-09-30. Produced by `scripts/run-eval.sh` (packaged eval runner).

**VERDICT: PASS — grading tests pass on disk (1/1 nodes).**

Claim under test: The base tool, given only the symptom report, produces a library fix that passes the real fix commit's grading tests on disk.

| Field | Value |
|---|---|
| Task | rich-u1-pretty-dataclass-unset-field — Rich: pretty-printing a dataclass with an unset field crashes |
| Tool / arm | claude / base |
| Model | opus |
| Success (disk-graded) | yes |
| Turns | 5 |
| Cost USD | 0.099218 — metered (tool JSON envelope) |
| Wall s | 31 |
| Grading python | /home/hatch/workspace/p2/secondcode/venv/bin/python (explicit (--python / EVAL_PYTHON)) |
| Source clone | /home/hatch/workspace/p2/secondcode/.infra/rich-src (parent b6f2f7aa5, fix 6055e2d8e) |
| Run dir | /home/hatch/workspace/p3/bigmodel/evals/scratch-run-eval/runs/rich-u1-pretty-dataclass-unset-field-claude-base-20260930-185447 |
| Diff stat (excl. setup + grading tests) |  1 file changed, 3 insertions(+), 1 deletion(-) |
| Pytest tail | .                                                                                                                                                                                                [100%] | 1 passed in 0.17s |

Agent's own summary (self-report — not the grade):

```
Fixed: `Console().print(BadDataclass())` now prints `BadDataclass()` instead of crashing.

**Root cause:** When `rich/pretty.py` builds the tree for a dataclass, it loops over every field with `repr=True` and reads each value with `getattr(obj, field.name)`. A field declared with `field(init=False)` and no default is never set on the instance, so reading it raised `AttributeError`.

**Change:** `rich/pretty.py:783-787`. The loop now skips fields the instance doesn't have (`if field.repr and hasattr(obj, field.name)`). Fields that are set are handled exactly as before. The `empty=f"{ClassName}()"` fallback already there covers the case where no fields are left.

**Verification:**
- Ran the reproduction by hand:
  - `pretty_repr(BadDataclass())` gives `'BadDataclass()'`, and `Console().print(BadDataclass())` prints `BadDataclass()`.
  - A dataclass with one set field and one unset field renders as `Mixed(a=1)`. Once the second field is assigned, it renders as `Mixed(a=1, b=2)`.
- `/home/hatch/workspace/p2/secondcode/venv/bin/python -m pytest tests/test_pretty.py -q`: 50 passed, 1 skipped.

I didn't add a new test file.
```
