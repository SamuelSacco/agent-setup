# RUN nx-t4-stochastic-block-model-sparse-diagonal — claude / orient

Date: 2026-09-30. Produced by `scripts/run-eval.sh` (packaged eval runner).

**VERDICT: FAIL — grading tests do not pass on disk.**

Claim under test: The base tool, given only the symptom report, produces a library fix that passes the real fix commit's grading tests on disk.

| Field | Value |
|---|---|
| Task | nx-t4-stochastic-block-model-sparse-diagonal — NetworkX: stochastic_block_model sparse path, diagonal blocks |
| Tool / arm | claude / orient |
| Model | opus |
| Success (disk-graded) | no |
| Turns | 14 |
| Cost USD | 0.316735 — metered (tool JSON envelope) |
| Wall s | 148 |
| Grading python | /home/hatch/workspace/p2/w3/scratch/venv/bin/python (explicit (--python / EVAL_PYTHON)) |
| Source clone | /home/hatch/workspace/p2/w3/scratch/.infra/nx-src (parent 17448435f, fix b3c9b00aa) |
| Run dir | /home/hatch/workspace/p3/bigmodel/evals/scratch-run-eval/runs/nx-t4-stochastic-block-model-sparse-diagonal-claude-orient-20260930-185026 |
| Diff stat (excl. setup + grading tests) |  |
| Pytest tail | FAILED networkx/generators/tests/test_community.py::test_sbm_sparse_applies_to_diagonal_blocks | FAILED networkx/generators/tests/test_community.py::test_stochastic_block_model | 2 failed in 0.22s |

Agent's own summary (self-report — not the grade):

```
I couldn't reproduce the reported bug, so I didn't change any library code. The checkout is back to baseline.

**What I found**
- In `stochastic_block_model` (`networkx/generators/community.py:627`), diagonal blocks never use the sparse method. Their edges are always drawn one pair at a time with `seed.random() < p[i][j]`. That uses up the edge iterator, so when the sparse loop runs afterwards it finds no edges left and adds nothing.
- So diagonal blocks already get exactly `p[i][i]` per edge, whether `sparse` is on or off. The only thing that differs from off-diagonal blocks is the sampling method.
- **The reported example:** `[75, 75]` with `[[0.25, 0.05], [0.05, 0.25]]` gives within-block densities of 0.245/0.238 (seed 0), 0.248/0.253 (seed 1) and 0.240/0.245 (seed 42). I also tried `directed` and `selfloops`: every value was between 0.238 and 0.262, and none was "well above 0.25".
- **Averages over 200 seeds:** within-block density 0.2491 and off-diagonal density 0.0503, with `sparse=True` and `sparse=False` alike. That is within sampling noise of the targets.

**What I tried and reverted**
I removed the extra per-pair loop so diagonal blocks would go through the sparse method too. The densities stayed correct (mean 0.2498), but:
- `test_stochastic_block_model` failed: it expects exactly `G.size() == 22160` for seed 0 and got 21842.
- The function's docstring example failed too: it expects block densities 0.245/0.348/0.405 and got 0.244/0.354/0.398.

Those fixed values ma
```
