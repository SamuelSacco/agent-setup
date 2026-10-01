# RUN nx-h4-k-components — claude / base

Date: 2026-10-01. X10 specialist A/B (pre-reg: `2026-10-01-X10-prereg.md`).

**VERDICT: FAIL — graded from disk by overlaying the real fix commit's tests (never agent self-report).**

| Field | Value |
|---|---|
| Task | nx-h4-k-components — NetworkX: k_components losing/truncating k-components |
| Tool / arm | claude / base |
| Model | claude-haiku-4-5-20251001 |
| Success (disk-graded) | no |
| Turns | 63 |
| Cost USD | 0.8540 — reconstructed from session-jsonl usage (envelope lost; see summary deviations) |
| Wall s | orphan-see-note |
| Grading nodes | 4 node IDs (see prereg) |
| Diff stat (excl. setup + grading tests) | 1 file changed, 8 insertions(+) |
| Pytest tail | FAILED networkx/algorithms/connectivity/tests/test_kcomponents.py::test_generate_partition_does_not_drop_cutset_nodes | 1 failed, 3 passed in 0.62s |

Agent's own summary (self-report — not the grade):

```
ENVELOPE LOST (exec session SIGTERM; claude child completed orphaned). Cost reconstructed from session jsonl usage at Haiku 4.5 list prices.
```
