# RUN nx-t5-betweenness-k-scaling — copilot / base

Date: 2026-10-01. Produced by `scripts/run-eval.sh` (packaged eval runner).

**VERDICT: PASS — grading tests pass on disk (2/2 nodes).**

Claim under test: The base tool, given only the symptom report, produces a library fix that passes the real fix commit's grading tests on disk.

| Field | Value |
|---|---|
| Task | nx-t5-betweenness-k-scaling — NetworkX: edge betweenness centrality scaling with k < n |
| Tool / arm | copilot / base |
| Model | claude-haiku-4-5-20251001 |
| Success (disk-graded) | yes |
| Turns | n/a (copilot does not report turns) |
| Cost USD | 3.0765 — upper-bound estimate (footer tokens at $1/M in, $5/M out; cached input at full rate) |
| Wall s | 373 |
| Grading python | /home/hatch/workspace/w4a-nx-t5/evals/scratch-run-eval/venv/bin/python (runner-bootstrapped venv (task requirements.txt)) |
| Source clone | /home/hatch/workspace/w4a-nx-t5/evals/scratch-run-eval/cache/nx-t5-betweenness-k-scaling-src (parent 4ec9e3abd, fix a802a27f5) |
| Run dir | /home/hatch/workspace/w4a-nx-t5/evals/scratch-run-eval/runs/nx-t5-betweenness-k-scaling-copilot-base-20261001-053700 |
| Diff stat (excl. setup + grading tests) |  1 file changed, 1 insertion(+), 1 deletion(-) |
| Pytest tail |   warnings.warn( | ..                                                                       [100%] | 2 passed in 0.47s |

Agent's own summary (self-report — not the grade):

```
 to edge betweenness centrality values, while the node version correctly applied it.

**What I Changed:**
Modified `/networkx/algorithms/centrality/betweenness.py` line 250 to pass the `k` parameter to `_rescale_e`:

```python
# Before:
betweenness = _rescale_e(
    betweenness, len(G), normalized=normalized, directed=G.is_directed()
)

# After:
betweenness = _rescale_e(
    betweenness, len(G), normalized=normalized, directed=G.is_directed(), k=k
)
```

**How It Works:**
- The `_rescale_e` function already has the logic to handle `k` sampling: `if k is not None: scale = scale * n / k`
- By passing `k`, the scaling formula becomes: `scale = base_scale * n / k`
- For unnormalized undirected graphs: `scale = 0.5 * n / k`
- For normalized graphs: normalization is applied first, then the `n/k` factor

**Verification:**
All tests pass, including:
- ✓ Original problem case: path_graph(3) with k=2 now returns {(0,1): 2.25, (1,2): 2.25} (9/4)
- ✓ Normalized: path_graph(3) with k=2 now returns {(0,1): 0.75, (1,2): 0.75} (3/4)  
- ✓ Full graph (k=None) behavior unchanged
- ✓ Directed graphs work correctly
- ✓ Weighted graphs work correctly
- ✓ Multigraphs work correctly
- ✓ Edge cases (k=1, k=n) work correctly
- ✓ Consistent with node betweenness centrality scaling
- ✓ All existing test cases continue to pass





Changes    +1 -1
Duration   6m 8s
Tokens     ↑ 2.9m (2.9m cached, 61.8k written) • ↓ 35.3k (14.1k reasoning)
Resume     copilot --resume=e7c62d33-c086-447b-8d1a-bcf7906e7e01

```
