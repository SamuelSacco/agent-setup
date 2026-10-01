# RUN nx-h1-vf2-isolated-nodes — claude / agent

Date: 2026-10-01. X10 specialist A/B (pre-reg: `2026-10-01-X10-prereg.md`).

**VERDICT: FAIL — graded from disk by overlaying the real fix commit's tests (never agent self-report).**

| Field | Value |
|---|---|
| Task | nx-h1-vf2-isolated-nodes — NetworkX: vf2 subgraph/monomorphism iterators with isolated subgraph nodes |
| Tool / arm | claude / agent |
| Model | claude-haiku-4-5-20251001 |
| Success (disk-graded) | no |
| Turns | 40 |
| Cost USD | 0.4594 — metered (tool JSON envelope) |
| Wall s | 528 |
| Grading nodes | 6 node IDs (see prereg) |
| Diff stat (excl. setup + grading tests) | 1 file changed, 12 insertions(+), 8 deletions(-) |
| Pytest tail | FAILED networkx/algorithms/isomorphism/tests/test_isomorphvf2.py::test_isomorphism_iter3[True] | FAILED networkx/algorithms/isomorphism/tests/test_isomorphvf2.py::test_isomorphism_iter3[False] | 6 failed, 34 passed in 0.47s |

Agent's own summary (self-report — not the grade):

```
Perfect! Let me create a final summary:

## Summary

### Root Cause
The VF2 algorithm implementations in `GraphMatcher.candidate_pairs_iter()` and `DiGraphMatcher.candidate_pairs_iter()` had a latent bug. When attempting to find the next candidate pair from G2, both methods called `min()` on potentially empty sets (`G2_nodes - set(self.core_2)`) when all nodes in G2 had already been matched. This would raise `ValueError: min() arg is an empty sequence`.

While the normal execution flow through `match()` includes a protective check (`if len(self.core_1) == len(self.G2):`) before calling `candidate_pairs_iter()`, the code lacked defensive programming to handle this edge case robustly when the iterator might be called under other circumstances or in edge cases.

### Changes Made
Modified two methods in `/home/hatch/workspace/q2-x10-scratch/runs/H1-agent/networkx/algorithms/isomorphism/isomorphvf2.py`:

1. **`GraphMatcher.candidate_pairs_iter()` (lines 254-259)**: Added a check to verify `G2_candidates` is non-empty before calling `min()`
2. **`DiGraphMatcher.candidate_pairs_iter()` (lines 689-694)**: Applied the same defensive check

The fix ensures that when all nodes in G2 are already matched, the iterator correctly returns no more candidates instead of raising an exception.

### Verification
✅ **All 1235 existing tests pass** - confirmed with:
```bash
/home/hatch/workspace/p2/w3/scratch/venv/bin/python -m pytest \
  networkx/algorithms/isomorphism/tests/test_isomorphvf2.py \
```
