# RUN nx-t6-is-aperiodic-strong-connectivity — copilot / base

Date: 2026-10-01. Produced by `scripts/run-eval.sh` (packaged eval runner).

**VERDICT: PASS — grading tests pass on disk (6/6 nodes).**

Claim under test: The base tool, given only the symptom report, produces a library fix that passes the real fix commit's grading tests on disk.

| Field | Value |
|---|---|
| Task | nx-t6-is-aperiodic-strong-connectivity — NetworkX: is_aperiodic on non-strongly-connected digraphs |
| Tool / arm | copilot / base |
| Model | claude-haiku-4-5-20251001 |
| Success (disk-graded) | yes |
| Turns | n/a (copilot does not report turns) |
| Cost USD | 2.6485 — upper-bound estimate (footer tokens at $1/M in, $5/M out; cached input at full rate) |
| Wall s | 408 |
| Grading python | /home/hatch/workspace/w4a-nx-t6/evals/scratch-run-eval/venv/bin/python (runner-bootstrapped venv (task requirements.txt)) |
| Source clone | /home/hatch/workspace/w4a-nx-t6/evals/scratch-run-eval/cache/nx-t6-is-aperiodic-strong-connectivity-src (parent ffaa9ef8d, fix 86e143dd8) |
| Run dir | /home/hatch/workspace/w4a-nx-t6/evals/scratch-run-eval/runs/nx-t6-is-aperiodic-strong-connectivity-copilot-base-20261001-054425 |
| Diff stat (excl. setup + grading tests) |  1 file changed, 8 insertions(+), 4 deletions(-) |
| Pytest tail |   warnings.warn( | ......                                                                   [100%] | 6 passed in 0.50s |

Agent's own summary (self-report — not the grade):

```
trong connectivity check** (line ~648):
   ```python
   if not nx.is_strongly_connected(G):
       raise nx.NetworkXError("is_aperiodic not defined for non-strongly-connected graphs")
   ```

2. **Updated docstring**:
   - Updated the "Raises" section to document the new error
   - Fixed the incorrect example about acyclic graphs
   - Added a new example showing that non-strongly-connected graphs raise an error
   - Updated the third example to use a correctly strongly-connected graph with non-coprime cycles

### Verification Results

✅ **All problem statement requirements met:**
- `nx.DiGraph([(1, 2), (2, 3)])` (plain path) now raises `NetworkXError`
- 3-cycle plus separate self-loop node now raises `NetworkXError`
- Single node with self-loop returns `True`
- Single node without self-loop returns `False`
- Strongly connected even-length cycles return `False`

✅ **All existing strongly-connected test cases pass:**
- `test_is_aperiodic_cycle` ✓
- `test_is_aperiodic_cycle2` ✓  
- `test_is_aperiodic_selfloop` ✓
- `test_is_aperiodic_undirected_raises` ✓
- `test_is_aperiodic_empty_graph` ✓

✅ **Backward compatibility maintained:**
- Undirected graphs still raise `NetworkXError`
- Empty graphs still raise `NetworkXPointlessConcept`
- The change is minimal and focused (8 insertions, 4 deletions in 1 file)





Changes    +9 -5
Duration   6m 41s
Tokens     ↑ 2.5m (2.4m cached, 50.2k written) • ↓ 29.7k (6.4k reasoning)
Resume     copilot --resume=dfc30ebf-0650-4c77-860f-02f807078ef7

```
