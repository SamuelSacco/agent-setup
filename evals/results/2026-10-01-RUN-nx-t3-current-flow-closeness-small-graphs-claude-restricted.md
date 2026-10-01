# RUN nx-t3-current-flow-closeness-small-graphs — claude / restricted (X1 toolset A/B)

Date: 2026-10-01. X1 runner (evals/scratch-x1/run_x1.py); protocol:
evals/results/2026-10-01-X1-toolset-ab.md.

**VERDICT: FAIL — grading tests do not pass on disk (1 node group, 4 parametrized cases).**

| Field | Value |
|---|---|
| Task | nx-t3-current-flow-closeness-small-graphs — NetworkX: current_flow_closeness_centrality on small graphs |
| Arm | restricted (6 tools: Read, Write, Edit, Bash, Grep, Glob) |
| Model | claude-haiku-4-5-20251001 |
| Success (disk-graded) | no |
| Turns | 11 |
| Cost USD | 0.286612 — metered (tool JSON envelope) |
| Wall s | 205 |
| Grading python | /home/hatch/workspace/p2/w3/scratch/venv/bin/python |
| Source clone | /home/hatch/workspace/p2/w3/scratch/.infra/nx-src (parent 65becad79, fix fc87a81fd) |

Reconstruction note: this file was rebuilt by the evaluator from the
runner's delivered JSON output after the execution layer's
filesystem divergence (see the incident section of
`2026-10-01-X1-toolset-ab.md`). Pass/fail, turns, and cost are the
runner's own disk-grading output, not agent self-report; the graded
run tree itself did not survive the divergence, so diff stat and
pytest tail are unavailable for this run.
