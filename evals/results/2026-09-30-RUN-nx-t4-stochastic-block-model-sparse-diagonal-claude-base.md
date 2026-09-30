# RUN nx-t4-stochastic-block-model-sparse-diagonal — claude / base

Date: 2026-09-30. Produced by `scripts/run-eval.sh` (packaged eval runner).

**VERDICT: FAIL — grading tests do not pass on disk.**

Claim under test: The base tool, given only the symptom report, produces a library fix that passes the real fix commit's grading tests on disk.

| Field | Value |
|---|---|
| Task | nx-t4-stochastic-block-model-sparse-diagonal — NetworkX: stochastic_block_model sparse path, diagonal blocks |
| Tool / arm | claude / base |
| Model | opus |
| Success (disk-graded) | no |
| Turns | 13 |
| Cost USD | 0.284851 — metered (tool JSON envelope) |
| Wall s | 199 |
| Grading python | /home/hatch/workspace/p2/w3/scratch/venv/bin/python (explicit (--python / EVAL_PYTHON)) |
| Source clone | /home/hatch/workspace/p2/w3/scratch/.infra/nx-src (parent 17448435f, fix b3c9b00aa) |
| Run dir | /home/hatch/workspace/p3/bigmodel/evals/scratch-run-eval/runs/nx-t4-stochastic-block-model-sparse-diagonal-claude-base-20260930-184700 |
| Diff stat (excl. setup + grading tests) |  |
| Pytest tail | FAILED networkx/generators/tests/test_community.py::test_sbm_sparse_applies_to_diagonal_blocks | FAILED networkx/generators/tests/test_community.py::test_stochastic_block_model | 2 failed in 0.25s |

Agent's own summary (self-report — not the grade):

```
I couldn't reproduce the bug on this checkout, so I haven't changed any library code. The working tree is back to the baseline.

**What I found**
- With sizes [75, 75] and p = [[0.25, 0.05], [0.05, 0.25]], within-block densities come out at or slightly below 0.25, not above. Seed 42 gives 0.240 and 0.245 (off-diagonal 0.048), and seeds 0–2 give 0.238–0.253.
- Sparse and non-sparse give identical diagonal edge counts in all four combinations of `directed` and `selfloops`. That's because of how the code is structured (`networkx/generators/community.py:627-640`): in the `i == j` branch, the diagonal blocks are always sampled by a plain per-edge loop, and that loop uses up the edge iterator. By the time the sparse code runs, there are no diagonal pairs left for it to add. So the sparse path never touches diagonal blocks and can't inflate them.
- The existing tests pass on the unmodified code (22 passed).

**What I tried and reverted**
I removed that per-edge loop so the sparse path would handle diagonal blocks too. The sparse path is itself unbiased: the mean diagonal density over 200 seeds was 0.2498. But it changes the output for a fixed seed. `test_stochastic_block_model` then got `G.size() == 21842` instead of the pinned 22160, and the docstring example failed too. Since you asked for minimal changes and no edits to existing tests, I put it back.

**What I ran**
- `/home/hatch/workspace/p2/w3/scratch/venv/bin/python -m pytest networkx/generators/tests/test_community.py -q` → 
```
