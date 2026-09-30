# P2 Copilot Orientation A/B — Pre-Registration

Written and committed BEFORE any run in this workstream. Date: 2026-09-30.
Purpose: Phase 2 measured the orientation effect on Claude only
(`evals/results/2026-09-30-P2-realcode-ab.md`: combined n=8, orientation
8/8 vs base 6/8). The talk is "one setup, two agents"; this measures the
same effect in Copilot CLI.

## Codebase and tasks

Same codebase as the Claude A/B: networkx/networkx @
`92f497e2eb8192d1ce9205595f512294e4a9b696`, mining clone at
`~/workspace/p2/w3/scratch/.infra/nx-src` (verified clean at the pin).
Same grading environment: Python 3.12 venv
`~/workspace/p2/w3/scratch/venv` (pytest 9.1.1, numpy 2.5.3,
scipy 1.18.1), library imported from the run's own checkout.

All 8 tasks from the Claude experiment are reused — the original batch
(T1–T4, definitions in `2026-09-30-P2-realcode-prereg.md`) and the
replication batch (R1–R4, definitions in the replication section of
`2026-09-30-P2-realcode-ab.md`). Every task was oracle-validated before
its original use: the real commit's tests pass at the commit and fail
at the parent with only the commit's test files overlaid.

| Task | Parent | Fix commit | Grading test node(s) |
|------|--------|-----------|----------------------|
| T1 ISMAGS empty candidates | `9ec50e84` | `c94928ed` | test_ismags.py::TestLargestCommonSubgraph::{test_largest_subgraph_null_graph_cases, test_largest_subgraph_empty_graphs, test_largest_subgraph_color_mismatches} |
| T2 SpanningTreeIterator next() | `5d160909` | `46a639ae` | test_mst.py::TestSpanningTreeIterator::test_next_without_iter |
| T3 current_flow small graphs | `65becad7` | `fc87a81f` | test_current_flow_closeness.py::TestFlowClosenessCentrality::test_current_flow_closeness_centrality_small_graphs (4 cases) |
| T4 SBM sparse diagonal | `17448435` | `b3c9b00a` | test_community.py::{test_sbm_sparse_applies_to_diagonal_blocks, test_stochastic_block_model} |
| R1 min_weighted_dominating_set cost fn | `6bf5e809` | `a9c8113b` | test_dominating_set.py::TestMinWeightDominatingSet::test_cost_accounts_for_already_dominated |
| R2 eccentricity/diameter/radius null graph | `fa512336` | `d3e01821` | test_distance_measures.py::TestDistance::{test_eccentricity, test_diameter_radius_empty_graph} |
| R3 find_cliques_recursive directed | `8ec80c76` | `5cfb44f7` | test_clique.py::TestCliques::test_find_cliques_directed |
| R4 graph_edit_distance self-loops | `6b57b277` | `9c17836f` | test_similarity.py::TestSimilarity::{test_one_node_one_loop_and_empty_graph, test_one_node_two_loops_and_empty_graph} |

Prompts: the operative files, byte-identical to the Claude runs —
`~/workspace/p2/w3/scratch/assets/prompt-T{1..4}.txt` and
`~/workspace/p2/portverify/repl/assets/prompt-R{1..4}.txt`.

## Arms

Tool: Copilot CLI 1.0.89 (`~/workspace/tools/bin/copilot`), BYOK
Anthropic, model `claude-haiku-4-5-20251001`, env per the W3 runner
(`COPILOT_PROVIDER_TYPE=anthropic`, base URL api.anthropic.com,
`COPILOT_ALLOW_ALL=true`), invoked `copilot -p '<prompt>'` with cwd =
the run checkout. Per-run wall-clock cap 900s (timeout kills, logged).

Each run starts from the task's parent commit, exported via
`git archive` into a fresh directory with a fresh single-commit
`git init` — no future history reachable from inside a run.

- **Copilot base:** fresh checkout + `.claude/settings.json` (the same
  inert file the W3 runs carried; Copilot does not read it). Nothing else.
- **Copilot +orientation:** identical, plus the frozen orientation text
  as `CLAUDE.md` at the checkout root — byte-identical copy of
  `assets/orientation.md` (Appendix of the Claude prereg; the two
  scratch copies diff-verified identical 2026-09-30). Same artifact,
  same filename, same placement as the Claude +orientation arm.
  Copilot CLI reads root `CLAUDE.md` natively (`docs/tips-copilot.md`).

**Reuse of W3 base runs.** W3 already ran Copilot base on T1 and T3
under this exact protocol (same CLI, model, prompts, isolation,
grading) and both passed (T1 ~$1.49, T3 ~$0.47 converted). Those two
results are reused as the base arm for T1/T3; no new base runs for
them. New runs: +orientation × 8 tasks, base × 6 tasks (T2, T4,
R1–R4) = 14 runs.

## Grading (disk only, never self-report)

After the agent exits, the evaluator copies the real commit's version
of the task's changed test file(s) over the run tree and runs the
grading node IDs with the pinned venv. Success = every grading test
passes (pytest exit 0).

Cheat checks, per run (the Claude base T1 run escaped its tree in W3):
- The mining clone's `git status --porcelain` is asserted empty before
  every run setup and re-checked after every run; any dirt is logged
  verbatim and the clone restored from git before continuing.
- The run tree's own diff (`git status --porcelain` + `git diff --stat
  HEAD`, excluding `.claude/`, `CLAUDE.md`, and overlaid test files) is
  recorded for every run. A claimed fix with an empty own-tree diff is
  a failure regardless of anything else.

## Metrics

Per run: success (binary, primary), wall seconds, token totals parsed
from the Copilot footer (`↑` input, `↓` output), and converted cost at
the W3 rates ($1/M input, $5/M output). Footer counts are rounded and
cached input is counted at the full input rate, so converted costs are
upper-bound estimates — same caveat as W3. Copilot reports no turns.

## Claim and threshold (n=8 tasks; descriptive, not powered)

Claim C — "orientation improves Copilot success on real code": same
rule as preregistered Claim B for Claude, applied over completed task
pairs (a pair = base result + +orientation result for the same task,
counting the reused W3 base results for T1/T3):

- PROVEN if +orientation solves ≥1 task base fails AND +orientation
  solves ≥ as many tasks overall as base.
- REFUTED if +orientation solves fewer tasks than base.
- Otherwise UNVERIFIABLE (equal totals with no discordant pair, or
  incomplete pairs).

Cost comparison reported as raw converted totals per arm; no threshold.

## Run order and stop rules

Pre-registered order (pairs kept adjacent; expected-expensive tasks
last; +orientation for T1/T3 first because their base results exist):

1. T1 +orient, T3 +orient
2. R2 base, R2 +orient
3. R1 base, R1 +orient
4. R3 base, R3 +orient
5. T2 base, T2 +orient
6. R4 base, R4 +orient
7. T4 base, T4 +orient

- Budget cap: $4.00 total converted cost across the 14 new runs. No
  new run starts once cumulative converted cost exceeds $3.40.
- Hard stop 13:15 ET: no new run starts after 12:55 ET. Partial
  results are reported as-is; incomplete pairs are excluded from the
  Claim C tally and listed as incomplete.
- If Copilot workspace trust gating blocks edits in a scratch dir,
  that is logged as an incident, not worked around silently.

## Artifacts

Runner, raw outputs, per-run results, and ledger preserved in
`~/workspace/p2/copilot-ab/` (`runner.py`, `runs/`, `ledger.tsv`).
Results: `evals/results/2026-09-30-P2-copilot-ab.md`.
