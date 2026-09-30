<!-- W2 triage lab (X15): re-run of the S17 package on the FULL DEFAULT PATH — no --source, no EVAL_PYTHON. Runner auto-cloned the source and bootstrapped the grading venv. Scratch tree: ~/workspace/p3/runscratch. Verdict: PASS, exit 0. -->

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
| Cost USD | 0.114501 — metered (tool JSON envelope) |
| Wall s | 167 |
| Grading python | /home/hatch/workspace/p3/runscratch/evals/scratch-run-eval/venv/bin/python (runner-bootstrapped venv (task requirements.txt)) |
| Source clone | /home/hatch/workspace/p3/runscratch/evals/scratch-run-eval/cache/nx-t2-spanning-tree-iterator-src (parent 5d160909e, fix 46a639aeb) |
| Run dir | /home/hatch/workspace/p3/runscratch/evals/scratch-run-eval/runs/nx-t2-spanning-tree-iterator-claude-base-20260930-183342 |
| Diff stat (excl. setup + grading tests) |  1 file changed, 3 insertions(+) |
| Pytest tail |   warnings.warn( | .                                                                        [100%] | 1 passed in 0.19s |

Agent's own summary (self-report — not the grade):

```
Perfect! All tests pass. Let me create a summary of the fix:

## Summary

**Root Cause:**
The `SpanningTreeIterator` class had an iterator protocol implementation bug. The `partition_queue` attribute was only initialized in `__iter__()`, not in `__init__()`. When someone called `next()` directly on a freshly constructed iterator (without first calling `iter()`), the attribute didn't exist, causing `AttributeError: 'SpanningTreeIterator' object has no attribute 'partition_queue'`.

**What Changed:**
Modified `/networkx/algorithms/tree/mst.py` (lines 1097-1107) in the `__next__()` method to add lazy initialization:
```python
if not hasattr(self, 'partition_queue'):
    self.__iter__()
```

This ensures the iterator is properly initialized on the first `next()` call, whether or not `iter()` was explicitly called beforehand.

**Verification:**
- ✅ All 81 existing tests pass (2 skipped)
- ✅ Direct `next()` calls on fresh iterators now work
- ✅ For loops still work (existing functionality preserved)
- ✅ Mixed `iter()` and `next()` usage works
- ✅ Iterator properly raises `StopIteration` when exhausted
```
