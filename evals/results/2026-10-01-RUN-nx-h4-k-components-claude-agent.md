# RUN nx-h4-k-components — claude / agent

Date: 2026-10-01. X10 specialist A/B (pre-reg: `2026-10-01-X10-prereg.md`).

**VERDICT: FAIL — graded from disk by overlaying the real fix commit's tests (never agent self-report).**

| Field | Value |
|---|---|
| Task | nx-h4-k-components — NetworkX: k_components losing/truncating k-components |
| Tool / arm | claude / agent |
| Model | claude-haiku-4-5-20251001 |
| Success (disk-graded) | no |
| Turns | 37 |
| Cost USD | 0.3732 — metered (tool JSON envelope) |
| Wall s | 370 |
| Grading nodes | 4 node IDs (see prereg) |
| Diff stat (excl. setup + grading tests) | 1 file changed, 16 insertions(+) |
| Pytest tail | =========================== short test summary info ============================ | FAILED networkx/algorithms/connectivity/tests/test_kcomponents.py::test_generate_partition_does_not_drop_cutset_nodes | 1 failed, 3 passed in 0.70s |

Agent's own summary (self-report — not the grade):

```
## Summary

**Root Cause:** The `_generate_partition` function loses or truncates k-components when processing graphs where all nodes have degree ≤ k (such as k-regular graphs). The algorithm was designed to:
1. Find "core" nodes with degree > k (not in any minimum cutset)
2. Find connected components of these core nodes
3. Add back cutset nodes that neighbor these components

For k-regular graphs (e.g., icosahedra, complete graphs), there are NO nodes with degree > k, so the algorithm finds zero components and returns nothing, causing valid k-components to be lost.

**Fix Applied:** Added a fallback mechanism in `_generate_partition()` that triggers when no components are found. The fallback:
1. Finds all nodes NOT in any minimum cutset
2. Finds connected components of these non-cutset nodes
3. Adds back cutset nodes that have neighbors in these components

This ensures k-regular and near-regular graphs are handled correctly while maintaining backward compatibility.

**Change Details:**
- **File:** `networkx/algorithms/connectivity/kcomponents.py`
- **Function:** `_generate_partition(G, cuts, k)` (lines 181-209)
- **Lines added:** 8 lines for fallback mechanism + clarifying comments
- **No API changes, no unrelated behavior modified**

**Verification:**
- ✅ All 31 existing tests pass
- ✅ Two icosahedra (5-connected) joined through bridge: correctly identifies both 5-components
- ✅ Petersen graph (3-regular): correctly identified as single 3-component
- ✅ Complete graphs K6 (
```
