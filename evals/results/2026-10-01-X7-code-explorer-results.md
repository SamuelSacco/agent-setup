# X7 Kill Test — code-explorer — Results

Date: 2026-10-01. Pre-registration:
`evals/results/2026-10-01-X7-code-explorer-prereg.md` (commit 1228f44,
written before any run). Protocol executed as registered: 4 paired
codebase-exploration tasks on the pinned NetworkX snapshot, identical
prompts and flags, one variable = `--agent code-explorer`, Claude Code
2.1.285, `claude-haiku-4-5-20251001`, disk grading only against the
prereg's fixed answer key (PASS = ≥4/5 checks, no fabrication).

## Verdict: UNVERIFIABLE

Prereg rule applied mechanically:

- PROVEN requires ≥1 discordant win for the agent arm: **none** (all
  4 pairs concordant passes).
- REFUTED (X7 kill rule verbatim: no discordant win AND agent cost
  ≥ base cost): **not met** — agent total cost $0.1526 < base $0.1970.
- Remaining case (equal passes, no discordant win, agent cheaper) is
  UNVERIFIABLE by the prereg.

code-explorer neither earns its place nor is killed by this test.

## Per-pair outcomes

| Task | Base | Agent | Checks base | Checks agent | Cost base | Cost agent | Turns base | Turns agent |
|------|------|-------|-------------|--------------|-----------|------------|------------|-------------|
| CE1 current_flow_closeness | PASS | PASS | 5/5 | 5/5 | $0.0243 | $0.0312 | 3 | 7 |
| CE2 ISMAGS largest_common_subgraph | PASS | PASS | 4/5 | 5/5 | $0.0833 | $0.0495 | 1 | 4 |
| CE3 stochastic_block_model sparse | PASS | PASS | 5/5 | 5/5 | $0.0436 | $0.0310 | 4 | 3 |
| CE4 SpanningTreeIterator | PASS | PASS | 5/5 | 5/5 | $0.0458 | $0.0409 | 3 | 3 |
| **Total** | **4/4** | **4/4** | mean 4.75 | mean 5.00 | **$0.1970** | **$0.1526** | 11 | 17 |

Discordant pairs: 0 in either direction. Fabrication flags: 0 in
either arm (see grading note). CE2 is the only sub-threshold
difference: base missed check (2) `create_aligned_partitions`
(4/5, still PASS); agent hit 5/5. Descriptive only — both arms pass,
so it is not a discordant pair.

Secondary (descriptive, no threshold per prereg): agent arm cost
−22.5% vs base in aggregate (cheaper on 3 of 4 pairs; CE1 agent cost
more, +28%, on +4 turns), turns +55% (17 vs 11) for equal passes.

## Grading note (fabrication check)

First grader pass flagged CE1-agent for the bare token
`flow_matrix.py` (cited as "(lines 36–80 in flow_matrix.py)"). The
same answer cites the full path
`networkx/algorithms/centrality/flow_matrix.py`, which exists. The
prereg defines fabrication as a cited path that does not exist in the
snapshot tree; a bare filename naming a file present in the tree is
not a fabrication. Grader corrected to the prereg wording (token
passes if the root-relative path exists OR a file with that basename
exists in the tree); re-grade: 0 fabrications in either arm. The
correction is recorded here and in `grade.py`; raw result texts are
unchanged on disk.

## Spend

Metered total $0.3496 (sum of `total_cost_usd` from the 8 JSON run
envelopes) of the $2.00 hard cap. No run exceeded the $0.60 single-run
soft cap (max $0.0833). All 8 runs completed, no timeouts, no
incomplete pairs.

## Artifacts

- Runner, grader, raw envelopes, result texts, ledger, grades:
  `~/workspace/w2c-x7-scratch/` (`runner.py`, `grade.py`, `runs/`,
  `ledger.tsv`, `grades.json`).
- Ledger: claim S25 in `docs/claims-ledger.md`.
- Backlog: X7 updated (code-explorer half) in
  `docs/experiments-backlog.md`; planner half unchanged.
- Deviation: one batch process running CE3-agent/CE4 was terminated
  (SIGTERM) by the harness after CE3-base; the remaining runs were
  executed individually in the registered order. No run was repeated
  and no grade changed.

## What would decide it

Harder exploration tasks with base headroom: at this difficulty the
base arm passes 4/4 at 4.75/5 mean checks, so no discordant pair is
reachable. A re-test needs tasks the base arm fails (deeper call
chains, ambiguous entry points) — same protocol, new task mining.
