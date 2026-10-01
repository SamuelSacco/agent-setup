# RUN nx-h6-edge-betweenness-k — claude / agent

Date: 2026-10-01. X10 specialist A/B (pre-reg: `2026-10-01-X10-prereg.md`).

**VERDICT: PASS — graded from disk by overlaying the real fix commit's tests (never agent self-report).**

| Field | Value |
|---|---|
| Task | nx-h6-edge-betweenness-k — NetworkX: edge betweenness centrality scaling when k<N |
| Tool / arm | claude / agent |
| Model | claude-haiku-4-5-20251001 |
| Success (disk-graded) | yes |
| Turns | 24 |
| Cost USD | 0.2880 — metered (tool JSON envelope) |
| Wall s | 199 |
| Grading nodes | 2 node IDs (see prereg) |
| Diff stat (excl. setup + grading tests) | 1 file changed, 1 insertion(+), 1 deletion(-) |
| Pytest tail |   warnings.warn( | ..                                                                       [100%] | 2 passed in 0.28s |

Agent's own summary (self-report — not the grade):

```
Perfect! All tests pass. Let me create a summary document:

## Summary

### Root Cause
The `edge_betweenness_centrality` function in `networkx/algorithms/centrality/betweenness.py` was not passing the `k` parameter (sampling parameter) to the `_rescale_e` function during the rescaling step. This caused the function to apply an incorrect scaling factor when `k < n` (sampling fewer nodes than the total number of nodes).

When sampling `k` nodes from `n` total nodes:
- The algorithm only computes shortest paths from the sampled nodes
- The raw edge betweenness accumulation is based on these k sources
- To estimate the full graph betweenness, the result must be scaled by `n/k` to account for the sampling

Without the `k` parameter, the rescaling function applied a fixed scale factor (e.g., 0.5 for undirected graphs) instead of the corrected scale (`0.5 * n/k` for undirected).

### What Was Changed
**File:** `networkx/algorithms/centrality/betweenness.py`

**Line 250-251:** Added `k=k` parameter to the `_rescale_e` function call:

```python
betweenness = _rescale_e(
    betweenness, len(G), normalized=normalized, directed=G.is_directed(), k=k
)
```

This single-line change ensures the `_rescale_e` function applies the correct scaling factor when sampling is used.

### What Was Verified
1. ✓ Original reported test case: `nx.path_graph(3)` with `k=2, seed=42` now returns correct results
2. ✓ All 96 existing tests pass without regression  
3. ✓ Full computation (k=None) continues to
```
