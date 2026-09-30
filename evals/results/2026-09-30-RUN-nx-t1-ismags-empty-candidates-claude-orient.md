# RUN nx-t1-ismags-empty-candidates — claude / orient

Date: 2026-09-30. Produced by `scripts/run-eval.sh` (packaged eval runner).

**VERDICT: PASS — grading tests pass on disk (3/3 nodes).**

Claim under test: The base tool, given only the symptom report, produces a library fix that passes the real fix commit's grading tests on disk.

| Field | Value |
|---|---|
| Task | nx-t1-ismags-empty-candidates — NetworkX: ISMAGS largest_common_subgraph, empty candidate sets |
| Tool / arm | claude / orient |
| Model | opus |
| Success (disk-graded) | yes |
| Turns | 9 |
| Cost USD | 0.194882 — metered (tool JSON envelope) |
| Wall s | 158 |
| Grading python | /home/hatch/workspace/p2/w3/scratch/venv/bin/python (explicit (--python / EVAL_PYTHON)) |
| Source clone | /home/hatch/workspace/p2/w3/scratch/.infra/nx-src (parent 9ec50e847, fix c94928ed9) |
| Run dir | /home/hatch/workspace/p3/bigmodel/evals/scratch-run-eval/runs/nx-t1-ismags-empty-candidates-claude-orient-20260930-183648 |
| Diff stat (excl. setup + grading tests) |  1 file changed, 3 insertions(+), 1 deletion(-) |
| Pytest tail |   warnings.warn( | ...                                                                      [100%] | 3 passed in 0.56s |

Agent's own summary (self-report — not the grade):

```
I fixed the crash: `largest_common_subgraph()` now returns an empty list when no subgraph node has a candidate match, instead of raising `ValueError`. All 103 existing ISMAGS tests pass.

**Root cause.** `largest_common_subgraph()` in `networkx/algorithms/isomorphism/ismags.py` checks `if any(candidate_sets.values())` before searching. Each value there is a *set of frozensets*: every node's candidate matches are stored as one or more frozensets, and its real candidates are what they have in common. A node with no candidates gets `{frozenset()}`, which still counts as true because the outer set isn't empty. So the check never stopped the search. In your reproduction no subgraph color exists in the graph, so the list of nodes to map ended up empty, and `_largest_common_subgraph` crashed calling `min()` on it.

**Change.** A one-line fix to that guard (plus a short comment): it now checks whether any subgraph node has a non-empty set of candidates:
```python
if any(frozenset.intersection(*cands) for cands in candidate_sets.values()):
```
If at least one node has candidates, the list of nodes to map is never empty, so the crash can't happen. Nothing changes when candidates exist.

**Self-loop case.** On this checkout it didn't crash before the fix; it already returned `[]`. The search still ran pointlessly, though, shrinking the subgraph one node at a time until a single node was left. With the fix it returns `[]` straight away.

**Verification:**
- A script running both reported
```
