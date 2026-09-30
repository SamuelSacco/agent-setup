# RUN nx-t2-spanning-tree-iterator — claude / base

Date: 2026-09-30. Produced by `scripts/run-eval.sh` (packaged eval runner).

**VERDICT: PASS — grading tests pass on disk (1/1 nodes).**

Claim under test: The base tool, given only the symptom report, produces a library fix that passes the real fix commit's grading test on disk.

| Field | Value |
|---|---|
| Task | nx-t2-spanning-tree-iterator — NetworkX: SpanningTreeIterator next() before iter() |
| Tool / arm | claude / base |
| Model | opus |
| Success (disk-graded) | yes |
| Turns | 6 |
| Cost USD | 0.127089 — metered (tool JSON envelope) |
| Wall s | 73 |
| Grading python | /home/hatch/workspace/p2/w3/scratch/venv/bin/python (explicit (--python / EVAL_PYTHON)) |
| Source clone | /home/hatch/workspace/p2/w3/scratch/.infra/nx-src (parent 5d160909e, fix 46a639aeb) |
| Run dir | /home/hatch/workspace/p3/bigmodel/evals/scratch-run-eval/runs/nx-t2-spanning-tree-iterator-claude-base-20260930-184427 |
| Diff stat (excl. setup + grading tests) |  1 file changed, 7 insertions(+) |
| Pytest tail |   warnings.warn( | .                                                                        [100%] | 1 passed in 0.29s |

Agent's own summary (self-report — not the grade):

```
I fixed it: `next()` on a freshly built `SpanningTreeIterator` now returns the first tree, and repeated calls give the same trees in the same order as a for loop.

**Root cause:** The priority queue of partitions (`self.partition_queue`) and the first minimum spanning tree were only set up inside `__iter__` (`networkx/algorithms/tree/mst.py:1078`). A for loop calls `__iter__` automatically; `next(it)` goes straight to `__next__`. So the queue didn't exist yet, and the first line of `__next__` failed with the `AttributeError`.

**Change:** At the top of `__next__` in `networkx/algorithms/tree/mst.py`, if the queue doesn't exist yet, it now calls `self.__iter__()` to set it up. There is one extra guard: when the iterator runs out it deletes `self.G` and the queue, so if `G` is also gone it raises `StopIteration` rather than trying to set up again. Without that, a `next()` after exhaustion would crash instead of stopping. Nothing else changed, including the public API and for-loop behaviour.

**Verification:**
- On a weighted `K4`, I called `next()` until `StopIteration`. It gave all 16 spanning trees, identical to the for-loop output, and one more `next()` still raised `StopIteration`.
- `python -m pytest networkx/algorithms/tree/tests/test_mst.py -q`: 81 passed, 2 skipped.

`ArborescenceIterator` in `networkx/algorithms/tree/branchings.py` has the same bug, because it also only sets up its queue in `__iter__`. I left it alone since the report only covers `SpanningTreeIterator`
```
