# RUN nx-t2-spanning-tree-iterator — claude / orient

Date: 2026-09-30. Produced by `scripts/run-eval.sh` (packaged eval runner).

**VERDICT: PASS — grading tests pass on disk (1/1 nodes).**

Claim under test: The base tool, given only the symptom report, produces a library fix that passes the real fix commit's grading test on disk.

| Field | Value |
|---|---|
| Task | nx-t2-spanning-tree-iterator — NetworkX: SpanningTreeIterator next() before iter() |
| Tool / arm | claude / orient |
| Model | opus |
| Success (disk-graded) | yes |
| Turns | 5 |
| Cost USD | 0.122968 — metered (tool JSON envelope) |
| Wall s | 62 |
| Grading python | /home/hatch/workspace/p2/w3/scratch/venv/bin/python (explicit (--python / EVAL_PYTHON)) |
| Source clone | /home/hatch/workspace/p2/w3/scratch/.infra/nx-src (parent 5d160909e, fix 46a639aeb) |
| Run dir | /home/hatch/workspace/p3/bigmodel/evals/scratch-run-eval/runs/nx-t2-spanning-tree-iterator-claude-orient-20260930-184548 |
| Diff stat (excl. setup + grading tests) |  1 file changed, 7 insertions(+) |
| Pytest tail |   warnings.warn( | .                                                                        [100%] | 1 passed in 0.19s |

Agent's own summary (self-report — not the grade):

```
Calling `next()` directly on a fresh `SpanningTreeIterator` now returns the first spanning tree, and repeated calls list all trees and then raise `StopIteration`. For loops work as before.

**Root cause:** in `networkx/algorithms/tree/mst.py`, all of the setup happened in `__iter__`: creating `self.partition_queue`, clearing old partition data, and computing the first minimum spanning tree. `__init__` never ran any of it. A for loop calls `iter()` before `next()`, so it worked. Calling `next()` directly skipped the setup, and `__next__` crashed on the missing `partition_queue`.

**Fix:** at the start of `__next__`, if `partition_queue` doesn't exist yet, it now runs `self.__iter__()` first. Two consequences:
- The setup still only happens when the first tree is requested, so creating the iterator stays cheap.
- If the iterator is already used up (`__next__` deletes `self.G` and the queue at that point), further `next()` calls raise `StopIteration` again. Before, they would have raised `AttributeError`.

No public API changed and no test files were edited.

**Verification:**
- On `complete_graph(4)` with distinct weights, calling `next()` until `StopIteration` produced all 16 trees, in the same order as a for loop. One more `next()` after that raised `StopIteration` again.
- `python -m pytest networkx/algorithms/tree/tests/test_mst.py -q`: 81 passed, 2 skipped.
```
