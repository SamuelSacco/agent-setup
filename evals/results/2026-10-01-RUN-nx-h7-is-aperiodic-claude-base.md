# RUN nx-h7-is-aperiodic — claude / base

Date: 2026-10-01. X10 specialist A/B (pre-reg: `2026-10-01-X10-prereg.md`).

**VERDICT: PASS — graded from disk by overlaying the real fix commit's tests (never agent self-report).**

| Field | Value |
|---|---|
| Task | nx-h7-is-aperiodic — NetworkX: is_aperiodic null/disconnected/single-node edge cases |
| Tool / arm | claude / base |
| Model | claude-haiku-4-5-20251001 |
| Success (disk-graded) | yes |
| Turns | 25 |
| Cost USD | 0.2732 — metered (tool JSON envelope) |
| Wall s | 240 |
| Grading nodes | 4 node IDs (see prereg) |
| Diff stat (excl. setup + grading tests) | 1 file changed, 4 insertions(+), 5 deletions(-) |
| Pytest tail |   warnings.warn( | ....                                                                     [100%] | 4 passed in 0.24s |

Agent's own summary (self-report — not the grade):

```
Perfect! The fix is complete and working correctly. Let me create a final summary:

## Summary

**Root cause:** The `is_aperiodic` function did not properly validate graph connectivity. It attempted to handle disconnected and weakly-connected graphs through recursive processing, but these cases are mathematically undefined for aperiodicity analysis, which requires a strongly connected graph.

**What I changed:** 
- Added a check at line 646-647 in `networkx/algorithms/dag.py` to raise `NetworkXError` if the graph is not strongly connected
- Simplified the return logic by removing the recursive case that tried to handle unvisited components, since now all graphs must be strongly connected (and thus all nodes will be visited in the BFS traversal)
- Updated the docstring to document that the function raises `NetworkXError` for non-strongly-connected graphs

**Behavior after fix:**
1. ✓ Empty graph → raises `NetworkXPointlessConcept`
2. ✓ Disconnected digraph with self-loop elsewhere → raises `NetworkXError`
3. ✓ Weakly-connected but not strongly-connected digraph → raises `NetworkXError`
4. ✓ Single-node digraph with self-loop → returns `True`
5. ✓ Aperiodic strongly-connected graphs → returns `True`
6. ✓ Periodic strongly-connected graphs → returns `False`

**Verification:** Ran the test suite with the prepared environment:
```
/home/hatch/workspace/p2/w3/scratch/venv/bin/python -m pytest networkx/algorithms/tests/test_dag.py -q
```
Result: 66 tests passed, 3 expected failures
```
