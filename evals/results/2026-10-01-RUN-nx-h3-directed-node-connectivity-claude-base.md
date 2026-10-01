# RUN nx-h3-directed-node-connectivity — claude / base

Date: 2026-10-01. X10 specialist A/B (pre-reg: `2026-10-01-X10-prereg.md`).

**VERDICT: FAIL — graded from disk by overlaying the real fix commit's tests (never agent self-report).**

| Field | Value |
|---|---|
| Task | nx-h3-directed-node-connectivity — NetworkX: node connectivity and node cuts for directed graphs |
| Tool / arm | claude / base |
| Model | claude-haiku-4-5-20251001 |
| Success (disk-graded) | no |
| Turns | 31 |
| Cost USD | 0.2972 — metered (tool JSON envelope) |
| Wall s | 183 |
| Grading nodes | 10 node IDs (see prereg) |
| Diff stat (excl. setup + grading tests) | 3 files changed, 27 insertions(+), 8 deletions(-) |
| Pytest tail | FAILED networkx/algorithms/connectivity/tests/test_cuts.py::test_directed_minimum_node_cut_not_strongly_connected | FAILED networkx/algorithms/connectivity/tests/test_cuts.py::test_directed_minimum_node_cut_both_orders | 5 failed, 5 passed in 0.34s |

Agent's own summary (self-report — not the grade):

```
Perfect! All tests pass. Let me create a summary of the changes:

## Summary

I've successfully fixed the `node_connectivity` and minimum node cut functions in NetworkX. Here's what was broken and how I fixed it:

### Root Causes

1. **Directed graphs not strongly connected**: The code only checked `is_weakly_connected()` for directed graphs, but should check `is_strongly_connected()`. A weakly-connected digraph that's not strongly connected has node connectivity 0.

2. **Self-loops inflating connectivity**: Self-loops were included in the auxiliary graph and counted toward degree calculations, but they don't represent actual connectivity between distinct nodes.

3. **Parallel edges and degree calculation**: The degree was calculated using `.degree()` which counts parallel edges and self-loops separately, but node connectivity should only depend on the existence of paths, not their multiplicity.

4. **Initial cutset including the selected node**: The initial minimum node cut included the node itself as a neighbor due to self-loops.

### Changes Made

**1. `/networkx/algorithms/connectivity/utils.py`**
- Skip self-loops when building the auxiliary node connectivity graph

**2. `/networkx/algorithms/connectivity/connectivity.py`**
- Changed directed graph check from `is_weakly_connected()` to `is_strongly_connected()`
- Changed degree calculation to count only distinct neighbors (excluding self-loops)

**3. `/networkx/algorithms/connectivity/cuts.py`**
- Changed directed graph
```
