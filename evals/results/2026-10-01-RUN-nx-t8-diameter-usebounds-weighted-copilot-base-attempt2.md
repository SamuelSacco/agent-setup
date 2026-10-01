# RUN nx-t8-diameter-usebounds-weighted — copilot / base

Date: 2026-10-01. Produced by `scripts/run-eval.sh` (packaged eval runner).

**VERDICT: FAIL — grading tests do not pass on disk.**

Claim under test: The base tool, given only the symptom report, produces a library fix that passes the real fix commit's grading tests on disk.

| Field | Value |
|---|---|
| Task | nx-t8-diameter-usebounds-weighted — NetworkX: diameter/radius/periphery/center with usebounds on weighted graphs |
| Tool / arm | copilot / base |
| Model | claude-haiku-4-5-20251001 |
| Success (disk-graded) | no |
| Turns | None |
| Cost USD | None — upper-bound estimate (footer tokens at $1/M in, $5/M out; cached input at full rate) |
| Wall s | 19 |
| Grading python | /home/hatch/workspace/w6-nx-t8/evals/scratch-run-eval/venv/bin/python (runner-bootstrapped venv (task requirements.txt)) |
| Source clone | /home/hatch/workspace/w6-nx-t8/evals/scratch-run-eval/cache/nx-t8-diameter-usebounds-weighted-src (parent 707d19536, fix c732e4346) |
| Run dir | /home/hatch/workspace/w6-nx-t8/evals/scratch-run-eval/runs/nx-t8-diameter-usebounds-weighted-copilot-base-20261001-062312 |
| Diff stat (excl. setup + grading tests) |  |
| Pytest tail | FAILED networkx/algorithms/tests/test_distance_measures.py::TestDistance::test_use_bounds_on_off_consistency[0.8-19-8] | FAILED networkx/algorithms/tests/test_distance_measures.py::TestDistance::test_use_bounds_on_off_consistency[0.8-19-9] | 500 failed in 12.58s |

Agent's own summary (self-report — not the grade):

```

400 Your credit balance is too low to access the Anthropic API. Please go to Plans & Billing to upgrade or purchase credits.


Changes    +0 -0
Duration   14s
Resume     copilot --resume=4f00683d-b07f-49cf-ae75-9bf53daa83d8

```
