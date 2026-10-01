# RUN nx-t2-spanning-tree-iterator — claude / full (X1 toolset A/B)

Date: 2026-10-01. X1 runner (evals/scratch-x1/run_x1.py); protocol: evals/results/2026-10-01-X1-toolset-ab.md.

**VERDICT: PASS — grading tests pass on disk (1 node group(s)).**

| Field | Value |
|---|---|
| Task | nx-t2-spanning-tree-iterator — NetworkX: SpanningTreeIterator next() before iter() |
| Arm | full (full default toolset) |
| Model | claude-haiku-4-5-20251001 |
| Success (disk-graded) | yes |
| Turns | None |
| Cost USD | None — metered (tool JSON envelope) |
| Wall s | 600 |
| Timed out | True |
| Grading python | /home/hatch/workspace/p2/w3/scratch/venv/bin/python |
| Source clone | /home/hatch/workspace/p2/w3/scratch/.infra/nx-src (parent 5d160909e, fix 46a639aeb) |
| Run dir | /home/hatch/workspace/w3-x1/evals/scratch-x1/runs/nx-t2-spanning-tree-iterator-claude-full-041843 |
| Diff stat (excl. setup + grading tests) |  1 file changed, 3 insertions(+) |
| Pytest tail |   warnings.warn( | .                                                                        [100%] | 1 passed in 0.23s |

Agent's own summary (self-report — not the grade):

```
UNPARSEABLE OUTPUT (timeout=True): 
```

Evaluator note (2026-10-01, X1 incident): this file is the ON-DISK
duplicate execution of this run, not the primary (delivered) series.
The backgrounded launch executed twice: the delivered execution
completed in 139 s with a parsed envelope (13 turns, $0.299612) and
graded FAIL; this on-disk duplicate hung, was killed by the runner's
600 s timeout (envelope lost, cost unmetered), and its tree — verified
by the evaluator, `mst.py` +3 lines, lazy `__iter__()` guard in
`__next__` — graded PASS. The pair's full-arm outcome is therefore
execution-dependent. Full accounting in
`evals/results/2026-10-01-X1-toolset-ab.md`.
