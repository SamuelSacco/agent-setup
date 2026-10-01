# X7 Kill Test — code-explorer — Pre-Registration

Written and committed BEFORE any agent eval run. Date: 2026-10-01.
Backlog item X7 (`docs/experiments-backlog.md`): planner /
code-explorer provisional roster entries earn their place. This file
covers **code-explorer only** (planner is a separate worker).
Branch: `wave2c/x7-code-explorer-kill-test` off master `e181f61`.

## Claim under test

"code-explorer (canonical specialist, read/search only) earns its
roster place: on codebase-exploration tasks it beats or matches the
base tool at no higher cost."

## Why the task type differs from S11 (recorded pre-run)

X7's cheapest-test line says "S11-protocol A/B". S11 graded
write/bugfix tasks by overlaying fix-commit tests. code-explorer as
emitted (`.claude/agents/code-explorer.md`) carries
`tools: [Read, Grep, Glob]` — it cannot write a fix, so a
write-graded A/B would fail the agent arm by construction and would
measure the tool restriction, not exploration quality. Adaptation,
decided pre-run: keep the S11 skeleton (4 paired tasks, identical
prompts, identical CLI flags, one variable = `--agent`, discordant-pair
rule, X7 kill rule verbatim, grading from disk only) and change only
the task class to the agent's target class — codebase exploration /
execution-path tracing, the work its canonical definition specifies
(entry-point discovery, path tracing, layer mapping, dependency
documentation). Grading artifacts are the evaluator-saved run
envelopes/result texts on disk plus existence checks against the
snapshot tree; agent self-report is never the grade (the saved result
text is the deliverable under test, scored by the evaluator's fixed
answer key below).

## Codebase snapshot

- NetworkX library tree at T1 parent `9ec50e847776e430f7957475ac52cbdceb462bf7`
  (same pin family as S11/S12), taken from the preserved prior run
  tree `~/workspace/p2/w3/scratch/runs/T1-base` (single-commit baseline
  `5cf05aa`). Verified pre-run by the evaluator: `git status` in that
  tree shows library code unmodified (only the S11 grading test file
  `test_ismags.py` differs, plus `.claude/` setup); no exploration
  check below touches that test file.
- Each run gets a fresh copy (snapshot minus `.git`/`.claude`),
  fresh single-commit `git init`. No fix history exists in the tree.

## Tasks (4) and answer key (evaluator-derived from disk, pre-run)

Each task: identical prompt to both arms (text in the runner,
`~/workspace/w2c-x7-scratch/runner.py`, frozen at prereg commit).
Each is scored on 5 factual checks (regex groups over the saved
result text, case-insensitive; any pattern in a group scores it).
Task PASS = ≥4/5 checks AND no fabrication (below).

- **CE1 — trace `current_flow_closeness_centrality`.**
  Checks: (1) file `current_flow_closeness` (.py);
  (2) `flow_matrix`; (3) any of `FullInverseLaplacian` /
  `SuperLUInverseLaplacian` / `CGInverseLaplacian`;
  (4) `laplacian_matrix`; (5) `reverse_cuthill_mckee`.
  Ground truth (grep/sed on snapshot): function at
  `networkx/algorithms/centrality/current_flow_closeness.py:16`;
  solvers imported from `.../flow_matrix.py` (classes at lines
  82/96/113); body calls `nx.laplacian_matrix` and
  `reverse_cuthill_mckee_ordering`.
- **CE2 — trace `ISMAGS.largest_common_subgraph`.**
  Checks: (1) `ismags`; (2) `create_aligned_partitions`;
  (3) `_get_node_color_candidate_sets`;
  (4) `analyze_subgraph_symmetry`; (5) `_largest_common_subgraph`.
  Ground truth: class `ismags.py:378`, method :806, `__init__` :550
  builds partitions via `create_aligned_partitions`; method :806
  calls `analyze_subgraph_symmetry`, `_get_node_color_candidate_sets`
  (:1016), then delegates to `_largest_common_subgraph` (:1266).
- **CE3 — trace `stochastic_block_model` sparse path.**
  Checks: (1) `community` (.py) or `stochastic_block_model`;
  (2) skip mechanism: `math.log` / `log(1` / `islice` + `skip`;
  (3) enumeration: `itertools.combinations` / `itertools.permutations`
  / `itertools.product` (any);
  (4) partition stored on graph: `graph["partition"]` /
  `graph['partition']` / `g.graph[` ;
  (5) `selfloops`.
  Ground truth: `networkx/generators/community.py:499`; sparse branch
  :640 computes `skip = floor(log(rand)/log(1-p))` and consumes via
  `itertools.islice`; diagonal enumeration uses
  combinations/permutations/product by directed/selfloops; partition
  read from `g.graph["partition"]` (:628).
- **CE4 — trace `SpanningTreeIterator`.**
  Checks: (1) `mst` (.py); (2) `partition_spanning_tree`;
  (3) `PriorityQueue` / `partition_queue`; (4) `EdgePartition`;
  (5) `_partition` or `_write_partition`.
  Ground truth: `networkx/algorithms/tree/mst.py:981` class;
  `__next__` :1082 lazily creates `PriorityQueue`, calls
  `partition_spanning_tree`; `_partition` :1113 splits with
  `EdgePartition.INCLUDED/EXCLUDED` (:30 enum).

- **Fabrication check (all tasks):** every `.py` path cited in the
  result text (backticked or bare token ending `.py`) must exist in
  the snapshot tree. Any cited path that does not exist = fabrication
  = task FAIL regardless of checks. (A path token is checked after
  stripping punctuation; tokens containing `*` are skipped as globs.)

## Arms

Same for every run: Claude Code 2.1.285 headless,
`claude -p '<prompt>' --model claude-haiku-4-5-20251001
--output-format json --permission-mode acceptEdits
--allowedTools 'Read Grep Glob Bash'`, scratch
`.claude/settings.json` = `{"apiKeyHelper": <vault helper>}`,
per-run wall cap 600 s. (No Write/Edit in either arm: the task is
answer-only; this also keeps the base arm from being graded on
edits. This is the one flag difference from S11, forced by the task
class and applied identically to both arms.)

- **Arm 1 — base:** fresh snapshot + settings.json only.
- **Arm 2 — +agent (code-explorer):** identical + the emitted agent
  file `.claude/agents/code-explorer.md` from master `e181f61`
  (adapter output, `tools: [Read, Grep, Glob]`) copied into the run
  tree's `.claude/agents/`; run adds `--agent code-explorer`.

Run order: CE1 base, CE1 agent, CE2 base, CE2 agent, CE3 base,
CE3 agent, CE4 base, CE4 agent (pairs adjacent, base first — same
order bias for every pair, recorded).

## Metrics

Per run: task PASS/FAIL (primary), checks hit (x/5), fabrication flag,
`num_turns` + `total_cost_usd` from the JSON envelope, wall seconds.
Per arm: tasks passed, total cost, total turns.

## Verdict rule (X7 kill rule, pre-registered)

Claim = "code-explorer earns its place".

- **PROVEN** (keep): agent passes ≥1 task base fails (discordant win)
  AND agent total passes ≥ base total passes.
- **REFUTED** (kill): agent passes fewer tasks than base, OR
  (no discordant win AND agent total cost ≥ base total cost) —
  the backlog X7 kill condition verbatim.
- **UNVERIFIABLE**: any other outcome (equal passes, no discordant
  win, agent cheaper; or incomplete pairs / harness errors).

Secondary, descriptive only: mean checks per task per arm; cost and
turn totals. No threshold on secondaries.

## Budget and stop rules

- Hard cap: $2.00 metered (Claude JSON envelopes) for this item.
- Single-run soft cap $0.60: a run passing it is killed and logged;
  its pair is incomplete → UNVERIFIABLE path unless the remaining
  pairs already decide the verdict under the rule above.
- No run starts if cumulative spend + $0.60 would exceed $2.00.
- Rigor (fresh tree per run, identical prompts, disk grading) is
  never shrunk.

## Artifacts

- Runner + prompts + raw envelopes + per-run grades:
  `~/workspace/w2c-x7-scratch/` (`runner.py`, `grade.py`, `runs/`,
  `ledger.tsv`, `grades.json`).
- Results: `evals/results/2026-10-01-X7-code-explorer-kill-test.md`.
- Ledger: new claim S25 (next free ID after S24) in
  `docs/claims-ledger.md`; backlog X7 updated in
  `docs/experiments-backlog.md` (code-explorer half only; planner
  half stays UNVERIFIABLE, separate worker).
