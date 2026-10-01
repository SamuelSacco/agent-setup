# RUN nx-h7-is-aperiodic — claude / agent

Date: 2026-10-01. X10 specialist A/B (pre-reg: `2026-10-01-X10-prereg.md`).

**VERDICT: FAIL — graded from disk by overlaying the real fix commit's tests (never agent self-report).**

| Field | Value |
|---|---|
| Task | nx-h7-is-aperiodic — NetworkX: is_aperiodic null/disconnected/single-node edge cases |
| Tool / arm | claude / agent |
| Model | claude-haiku-4-5-20251001 |
| Success (disk-graded) | no |
| Turns | 19 |
| Cost USD | 0.2349 — metered (tool JSON envelope) |
| Wall s | 207 |
| Grading nodes | 4 node IDs (see prereg) |
| Diff stat (excl. setup + grading tests) | 1 file changed, 4 insertions(+), 2 deletions(-) |
| Pytest tail | =========================== short test summary info ============================ | FAILED networkx/algorithms/tests/test_dag.py::test_is_aperiodic_weakly_connected_raises | 1 failed, 3 passed in 0.34s |

Agent's own summary (self-report — not the grade):

```
Credit balance is too low
```
