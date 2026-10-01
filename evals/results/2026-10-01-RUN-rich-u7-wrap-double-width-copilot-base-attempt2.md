# RUN rich-u7-wrap-double-width — copilot / base

Date: 2026-10-01. Produced by `scripts/run-eval.sh` (packaged eval runner).

**VERDICT: FAIL — grading tests do not pass on disk.**

Claim under test: The base tool, given only the symptom report, produces a library fix that passes the real fix commit's grading tests on disk.

| Field | Value |
|---|---|
| Task | rich-u7-wrap-double-width — Rich: wrapping drops double-width characters |
| Tool / arm | copilot / base |
| Model | claude-haiku-4-5-20251001 |
| Success (disk-graded) | no |
| Turns | None |
| Cost USD | None — upper-bound estimate (footer tokens at $1/M in, $5/M out; cached input at full rate) |
| Wall s | 30 |
| Grading python | /home/hatch/workspace/w6-rich-u7/evals/scratch-run-eval/venv/bin/python (runner-bootstrapped venv (task requirements.txt)) |
| Source clone | /home/hatch/workspace/w6-rich-u7/evals/scratch-run-eval/cache/rich-u7-wrap-double-width-src (parent b32e42bda, fix 59b1aca63) |
| Run dir | /home/hatch/workspace/w6-rich-u7/evals/scratch-run-eval/runs/rich-u7-wrap-double-width-copilot-base-20261001-061207 |
| Diff stat (excl. setup + grading tests) |  |
| Pytest tail | FAILED tests/test_cells.py::test_chop_cells_mixed_width - AssertionError: ass... | FAILED tests/test_text.py::test_wrap_cjk_mixed - AssertionError: assert '123... | 4 failed in 0.51s |

Agent's own summary (self-report — not the grade):

```

400 Your credit balance is too low to access the Anthropic API. Please go to Plans & Billing to upgrade or purchase credits.


Changes    +0 -0
Duration   22s
Resume     copilot --resume=38f26c88-881d-4548-af23-1607c74a3208

```
