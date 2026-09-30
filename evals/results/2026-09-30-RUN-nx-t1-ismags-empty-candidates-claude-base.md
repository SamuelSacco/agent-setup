# RUN nx-t1-ismags-empty-candidates — claude / base

Date: 2026-09-30. Produced by `scripts/run-eval.sh` (packaged eval runner).

**VERDICT: PASS — grading tests pass on disk (3/3 nodes).**

Claim under test: The base tool, given only the symptom report, produces a library fix that passes the real fix commit's grading tests on disk.

| Field | Value |
|---|---|
| Task | nx-t1-ismags-empty-candidates — NetworkX: ISMAGS largest_common_subgraph, empty candidate sets |
| Tool / arm | claude / base |
| Model | opus |
| Success (disk-graded) | yes |
| Turns | 9 |
| Cost USD | 0.189683 — metered (tool JSON envelope) |
| Wall s | 115 |
| Grading python | /home/hatch/workspace/p2/w3/scratch/venv/bin/python (explicit (--python / EVAL_PYTHON)) |
| Source clone | /home/hatch/workspace/p2/w3/scratch/.infra/nx-src (parent 9ec50e847, fix c94928ed9) |
| Run dir | /home/hatch/workspace/p3/bigmodel/evals/scratch-run-eval/runs/nx-t1-ismags-empty-candidates-claude-base-20260930-183435 |
| Diff stat (excl. setup + grading tests) |  1 file changed, 7 insertions(+), 3 deletions(-) |
| Pytest tail |   warnings.warn( | ...                                                                      [100%] | 3 passed in 0.28s |

Agent's own summary (self-report — not the grade):

```
Both reported cases now return `[]` instead of crashing, and the existing ISMAGS tests pass.

**Root cause:** In `ISMAGS.largest_common_subgraph()` (`networkx/algorithms/isomorphism/ismags.py`), the guard `if any(candidate_sets.values())` never stopped anything. Each value there is a set of frozensets, e.g. `{frozenset()}`, and that set counts as true even when the frozenset inside it is empty. So the search always ran:
- **Color case:** no subgraph color appears in the graph, so the starting node set was built as `frozenset()`. `min()` over that empty set raised the `ValueError`.
- **Self-loop case:** colors matched, but every node had an empty candidate set. The search still started, even though no node could ever be matched.

**Change:** I replaced that guard and the color-based starting set with one step. It collects the subgraph nodes whose candidate sets are all non-empty, returns nothing if there are none, and otherwise uses them as the starting set. A node with no candidates can't be part of any common subgraph, so leaving it out doesn't change results. This covers both the color and self-loop triggers, plus mixed cases where only some nodes can be matched.

**Verification:**
- A script with both reproductions: each now prints `[]`.
- A mixed case (a path graph with self-loops on two nodes against `path_graph(4)`) gives the expected 3-node matches, and `path_graph(5)` against itself still gives one match.
- `/home/hatch/workspace/p2/w3/scratch/venv/bin/python -m pytes
```
