# RUN nx-h6-edge-betweenness-k — claude / base

Date: 2026-10-01. X10 specialist A/B (pre-reg: `2026-10-01-X10-prereg.md`).

**VERDICT: PASS — graded from disk by overlaying the real fix commit's tests (never agent self-report).**

| Field | Value |
|---|---|
| Task | nx-h6-edge-betweenness-k — NetworkX: edge betweenness centrality scaling when k<N |
| Tool / arm | claude / base |
| Model | claude-haiku-4-5-20251001 |
| Success (disk-graded) | yes |
| Turns | 19 |
| Cost USD | 0.2097 — metered (tool JSON envelope) |
| Wall s | 201 |
| Grading nodes | 2 node IDs (see prereg) |
| Diff stat (excl. setup + grading tests) | 1 file changed, 1 insertion(+), 1 deletion(-) |
| Pytest tail |   warnings.warn( | ..                                                                       [100%] | 2 passed in 0.18s |

Agent's own summary (self-report — not the grade):

```
Perfect! All tests pass. Let me create a summary:

## Summary

**Root Cause:**  
The `edge_betweenness_centrality` function failed to pass the `k` parameter to the `_rescale_e` helper function (line 250-252). This prevented the sampling adjustment factor `n/k` from being applied when `k < n`, causing incorrect scaling of results.

**The Fix:**  
Added `k=k` to the `_rescale_e` call in `edge_betweenness_centrality` at line 251:

```python
betweenness = _rescale_e(
    betweenness, len(G), normalized=normalized, directed=G.is_directed(), k=k
)
```

**Verification:**
- ✓ Both problem examples now work correctly:
  - `nx.edge_betweenness_centrality(nx.path_graph(3), k=2, seed=42, normalized=False)` → `{(0,1): 9/4, (1,2): 9/4}`
  - `nx.edge_betweenness_centrality(nx.path_graph(3), k=2, seed=42, normalized=True)` → `{(0,1): 3/4, (1,2): 3/4}`
- ✓ All 96 existing tests pass
- ✓ Handles edge cases: full computations, directed/undirected graphs, weighted graphs, various k values, normalization consistency
```
