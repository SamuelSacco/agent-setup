# RUN nx-t7-network-simplex-faux-inf — copilot / base

Date: 2026-10-01. Produced by `scripts/run-eval.sh` (packaged eval runner).

**VERDICT: FAIL — grading tests do not pass on disk.**

Claim under test: The base tool, given only the symptom report, produces a library fix that passes the real fix commit's grading tests on disk.

| Field | Value |
|---|---|
| Task | nx-t7-network-simplex-faux-inf — NetworkX: network_simplex spurious unboundedness on feasible instances |
| Tool / arm | copilot / base |
| Model | claude-haiku-4-5-20251001 |
| Success (disk-graded) | no |
| Turns | None |
| Cost USD | None — upper-bound estimate (footer tokens at $1/M in, $5/M out; cached input at full rate) |
| Wall s | 22 |
| Grading python | /home/hatch/workspace/w6-nx-t7/evals/scratch-run-eval/venv/bin/python (runner-bootstrapped venv (task requirements.txt)) |
| Source clone | /home/hatch/workspace/w6-nx-t7/evals/scratch-run-eval/cache/nx-t7-network-simplex-faux-inf-src (parent f87c3611d, fix 7768b9273) |
| Run dir | /home/hatch/workspace/w6-nx-t7/evals/scratch-run-eval/runs/nx-t7-network-simplex-faux-inf-copilot-base-20261001-061424 |
| Diff stat (excl. setup + grading tests) |  |
| Pytest tail | =========================== short test summary info ============================ | FAILED networkx/algorithms/flow/tests/test_networksimplex.py::test_network_simplex_large_capacities[False-False-False] | 1 failed, 8 passed in 0.20s |

Agent's own summary (self-report — not the grade):

```

400 Your credit balance is too low to access the Anthropic API. Please go to Plans & Billing to upgrade or purchase credits.


Changes    +0 -0
Duration   17s
Resume     copilot --resume=0ca5b144-426f-4b6b-857e-e497664e2ee1

```
