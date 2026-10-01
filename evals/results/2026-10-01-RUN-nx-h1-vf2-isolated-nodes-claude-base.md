# RUN nx-h1-vf2-isolated-nodes — claude / base

Date: 2026-10-01. X10 specialist A/B (pre-reg: `2026-10-01-X10-prereg.md`).

**VERDICT: PASS — graded from disk by overlaying the real fix commit's tests (never agent self-report).**

| Field | Value |
|---|---|
| Task | nx-h1-vf2-isolated-nodes — NetworkX: vf2 subgraph/monomorphism iterators with isolated subgraph nodes |
| Tool / arm | claude / base |
| Model | claude-haiku-4-5-20251001 |
| Success (disk-graded) | yes |
| Turns | 40 |
| Cost USD | 0.4419 — metered (tool JSON envelope) |
| Wall s | 421 |
| Grading nodes | 6 node IDs (see prereg) |
| Diff stat (excl. setup + grading tests) | 1 file changed, 20 insertions(+), 9 deletions(-) |
| Pytest tail |   warnings.warn( | ........................................                                 [100%] | 40 passed in 0.43s |

Agent's own summary (self-report — not the grade):

```
Perfect! All tests pass. Let me verify the changes one final time and summarize:

## Summary

I've successfully fixed the VF2 graph isomorphism implementation to properly handle subgraph and monomorphism iteration with isolated nodes. The fix addresses two related bugs:

### Root Cause 1: Incorrect completion condition in `match()` method

The original code used the same completion condition for all matching types:
```python
if len(self.core_1) == len(self.G2):
    yield self.mapping
```

This is correct for subgraph/monomorphism matching (where only G2 needs to be fully matched), but **incorrect for graph isomorphism** (where both graphs must be fully matched). When G2 is empty and G1 is not, this condition causes immediate yielding of an empty mapping.

**Fix**: Distinguish between test types (lines 333-338):
```python
if self.test == "graph":
    complete = len(self.core_1) == len(self.G1) == len(self.G2)
else:  # subgraph or monomorphism
    complete = len(self.core_1) == len(self.G2)
```

### Root Cause 2: ValueError in `candidate_pairs_iter()` with empty sets

The method attempted `min(G2_nodes - set(self.core_2))` without checking if the set is empty, causing ValueError when all G2 nodes are matched.

**Fix**: Added guard checks in both `GraphMatcher` (line 254-256) and `DiGraphMatcher` (line 696-698):
```python
G2_remaining = G2_nodes - set(self.core_2)
if G2_remaining:
    other_node = min(G2_remaining, key=min_key)
    # ... yield pairs
```

### Verification
- All e
```
