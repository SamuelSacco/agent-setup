# RUN nx-t2-spanning-tree-iterator — claude / base

Date: 2026-09-30. Produced by `scripts/run-eval.sh` (packaged eval runner).

**VERDICT: PASS — grading tests pass on disk (1/1 nodes).**

Claim under test: The base tool, given only the symptom report, produces a library fix that passes the real fix commit's grading test on disk.

| Field | Value |
|---|---|
| Task | nx-t2-spanning-tree-iterator — NetworkX: SpanningTreeIterator next() before iter() |
| Tool / arm | claude / base |
| Model | claude-haiku-4-5-20251001 |
| Success (disk-graded) | yes |
| Turns | 11 |
| Cost USD | 0.10302575000000001 — metered (tool JSON envelope) |
| Wall s | 151 |
| Grading python | /home/hatch/workspace/p2/w3/scratch/venv/bin/python (explicit (--python / EVAL_PYTHON)) |
| Source clone | /home/hatch/workspace/p2/w3/scratch/.infra/nx-src (parent 5d160909e, fix 46a639aeb) |
| Run dir | /home/hatch/workspace/phase2/feedback-loop/evals/scratch-run-eval/runs/nx-t2-spanning-tree-iterator-claude-base-20260930-151609 |
| Diff stat (excl. setup + grading tests) |  1 file changed, 3 insertions(+) |
| Pytest tail |   warnings.warn( | .                                                                        [100%] | 1 passed in 0.15s |

Agent's own summary (self-report — not the grade):

```
Perfect! Here's a summary of the fix:

## Summary

**Root Cause:** The `SpanningTreeIterator` class initialized `partition_queue` only in `__iter__()`, which is not automatically called when `next()` is invoked directly on a fresh iterator. Python's iterator protocol only calls `__next__()` in direct `next()` calls, not `__iter__()`.

**What Changed:** Added a check in `__next__()` (lines 1105-1106 in mst.py) that initializes the iterator via `__iter__()` if `partition_queue` hasn't been created yet:

```python
if not hasattr(self, "partition_queue"):
    self.__iter__()
```

This is a minimal, non-breaking change that:
- Enables direct `next()` calls on fresh iterators  
- Preserves backward compatibility with for loops
- Maintains lazy initialization (queue only created when iteration starts)
- Follows Python's iterator protocol correctly

**Verification:**
- ✅ All 81 existing tests in `test_mst.py` pass (2 skipped)
- ✅ Direct `next()` calls work correctly for all spanning trees
- ✅ For loop iteration still works as before
- ✅ Both minimum and maximum spanning tree iteration work
```
