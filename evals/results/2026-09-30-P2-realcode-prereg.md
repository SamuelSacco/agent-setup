# P2 Real-Codebase A/B Eval — Pre-Registration

Written and committed BEFORE any agent eval run. Date: 2026-09-30.
Workstream W3, Phase 2 agent-setup project. Raw data deliverable; no
presentation framing.

## Codebase

- **networkx/networkx** (GitHub), pinned HEAD
  `92f497e2eb8192d1ce9205595f512294e4a9b696` (2026-09-28).
- Size at HEAD: ~121k LOC library source (`networkx/`, excluding tests),
  ~77k LOC tests. Pure Python; pytest suite with tests colocated in
  `tests/` subdirectories next to modules. Actively maintained (commits
  within 48h of pinning).
- Why: real git history with many small, same-commit bugfix+test pairs;
  targeted test files run in <2s; no build step, no network, no services.
- Grading environment (pinned): Python 3.12 venv at
  `scratch/venv` — pytest 9.1.1, numpy 2.5.3, scipy 1.18.1. Library is
  imported from the run's own checkout (repo root on sys.path via pytest
  rootdir), never installed.

## Task selection method

1. Scanned the last 400 non-merge commits at pinned HEAD.
2. Filter: subject marks a bug fix (BUG/fix); 3–90 changed lines in
   non-test `.py` files; ≤3 non-test files; ≥5 changed lines in test
   `.py` files in the SAME commit.
3. Picked 4 survivors spanning 4 different subsystems (isomorphism,
   tree, centrality, generators), each with a symptom reproducible in
   ≤15 lines at the parent commit.
4. Oracle validation (done pre-registration, no agents involved): for
   each task, the real commit's target tests were run (a) at the commit
   — all pass; (b) at the parent with only the commit's test files
   overlaid — the discriminating tests fail. Results:

| Task | At commit | At parent + commit tests |
|------|-----------|--------------------------|
| T1 ISMAGS | 3 passed | 2 failed, 1 passed |
| T2 SpanningTreeIterator | 1 passed | 1 failed (AttributeError, mst.py:1105) |
| T3 current_flow_closeness | 4 passed | 3 failed, 1 passed |
| T4 stochastic_block_model | 2 passed | 2 failed |

## Tasks (exact)

Each run starts from the task's PARENT commit, exported via
`git archive` into a fresh directory with a fresh single-commit
`git init` — the scratch tree contains no future history, so the real
fix is not reachable from inside a run.

### T1 — ISMAGS largest_common_subgraph, empty candidate sets
- Real commit `c94928ed94899033126c9d47f797a1f698584b20`;
  parent `9ec50e847776e430f7957475ac52cbdceb462bf7`.
- Grading tests (all must pass):
  `networkx/algorithms/isomorphism/tests/test_ismags.py::TestLargestCommonSubgraph::test_largest_subgraph_null_graph_cases`,
  `::test_largest_subgraph_empty_graphs`,
  `::test_largest_subgraph_color_mismatches`.
- Verified parent symptom: `ValueError: min() iterable argument is empty`
  from `largest_common_subgraph()` when no subgraph node has a candidate
  match (color mismatch reproduction, see prompt).

### T2 — SpanningTreeIterator next() before iter()
- Real commit `46a639aeb9bd4db8da444bd6a532df567b9a73cc`;
  parent `5d160909eeb42e9844496dd2bbd19b826d2242d7`.
- Grading test:
  `networkx/algorithms/tree/tests/test_mst.py::TestSpanningTreeIterator::test_next_without_iter`.
- Verified parent symptom: `AttributeError: 'SpanningTreeIterator'
  object has no attribute 'partition_queue'`.

### T3 — current_flow_closeness_centrality on small graphs
- Real commit `fc87a81fd3de0f17c03e611fd6e746994c66277c`;
  parent `65becad79fd10dff170b49fa003a6052c291d27d`.
- Grading test (4 parametrized cases, all must pass):
  `networkx/algorithms/centrality/tests/test_current_flow_closeness.py::TestFlowClosenessCentrality::test_current_flow_closeness_centrality_small_graphs`.
- Verified parent symptoms: empty graph → `NetworkXPointlessConcept`;
  single node (± self-loop) → `ZeroDivisionError`; path_graph(2) →
  `{0: 1.0, 1: 1.0}` (already correct).

### T4 — stochastic_block_model sparse path, diagonal blocks
- Real commit `b3c9b00aaab32ed74e5be79bf5960772d3e63467`;
  parent `17448435f2cac33018ceabba4d5faabdae768f0f`.
- Grading tests (both must pass):
  `networkx/generators/tests/test_community.py::test_sbm_sparse_applies_to_diagonal_blocks`,
  `networkx/generators/tests/test_community.py::test_stochastic_block_model`
  (the real commit also changed this existing test's expected values).
- Parent symptom: with the sparse heuristic active, realized
  within-community (diagonal) block density is systematically above the
  requested `p` under a fixed seed; off-diagonal densities are correct.

## Prompt (verbatim template; only SYMPTOM and VERIFY differ per task)

```
You are working in a fresh checkout of NetworkX, a Python library for
graphs (package code in `networkx/`, tests in `tests/` subdirectories
next to the modules).

Problem report:
<SYMPTOM>

Investigate, find the root cause, and fix it in the library code so the
reported behavior is correct in general, not just for the examples
above. Rules:
- Do not edit existing files under any `tests/` directory. You may add
  new test files if you want, but grading uses an external test suite.
- Keep the change minimal and consistent with the surrounding code
  style; do not change public APIs or unrelated behavior.
- Verify your fix by running the relevant existing tests from the repo
  root with the prepared environment:
  /home/hatch/workspace/p2/w3/scratch/venv/bin/python -m pytest <VERIFY> -q
  Do not install packages.
- When finished, give a short summary: root cause, what you changed,
  and what you ran to verify.
```

SYMPTOM texts:

- T1: "`ISMAGS.largest_common_subgraph()` crashes when no subgraph node
  has a candidate match in the graph. Reproduction: build ISMAGS on two
  `nx.path_graph(5)` graphs where every subgraph node carries the
  attribute `color='blue'` and the graph nodes carry no color, using
  `node_match=nx.isomorphism.categorical_node_match('color', None)`.
  Calling `list(ismags.largest_common_subgraph())` raises
  `ValueError: min() iterable argument is empty` instead of simply
  yielding no results; there is no common subgraph in that situation,
  so the expected result is an empty list. A related trigger: a graph
  in which every node has a self-loop, matched against a subgraph
  without self-loops, should likewise yield no results, not crash.
  Ordinary matching cases must keep working."
  VERIFY: networkx/algorithms/isomorphism/tests/test_ismags.py
- T2: "`next()` on a freshly constructed `SpanningTreeIterator` raises
  `AttributeError: 'SpanningTreeIterator' object has no attribute
  'partition_queue'` when `iter()` has not been called first (i.e. the
  iterator is used via `next(it)` directly instead of a for loop).
  Expected: `next(nx.SpanningTreeIterator(G))` returns the first
  spanning tree, exactly as iterating does, and repeated `next()` calls
  enumerate trees until `StopIteration`. Iterating with a for loop
  already works and must keep working."
  VERIFY: networkx/algorithms/tree/tests/test_mst.py
- T3: "`nx.current_flow_closeness_centrality` (information centrality)
  fails on very small graphs. An empty graph raises
  `NetworkXPointlessConcept`, and a graph with a single node — with or
  without a self-loop — raises `ZeroDivisionError`. Expected results:
  empty graph -> `{}`; single node -> `{0: 1.0}` (the self-loop case
  likewise `{0: 1.0}`). A 2-node path already returns
  `{0: 1.0, 1: 1.0}` and must keep doing so; results for larger graphs
  must be unchanged."
  VERIFY: networkx/algorithms/centrality/tests/test_current_flow_closeness.py
- T4: "`nx.stochastic_block_model` produces within-community
  (diagonal-block) densities that are systematically too high when it
  uses its sparse heuristic path. With a fixed seed the effect is
  deterministic: for example with sizes [75, 75] and
  p = [[0.25, 0.05], [0.05, 0.25]], the realized within-block
  densities come out well above 0.25, while the off-diagonal density
  is correct. Expected: the sparse path applies the same per-edge
  probability to diagonal blocks as to off-diagonal blocks."
  VERIFY: networkx/generators/tests/test_community.py

## Arms

Same model for every Claude run: `claude-haiku-4-5-20251001`,
Claude Code 2.1.285, headless
`claude -p '<prompt>' --output-format json --permission-mode acceptEdits
--allowedTools 'Write Edit Bash Read Glob Grep'`, scratch project
`.claude/settings.json` =
`{"apiKeyHelper": "/home/hatch/workspace/skills/anthropic/bin/claude_api_key_helper.py"}`.
Per-run wall-clock cap 900s (timeout kills and is logged).

- **Arm 1 — base:** scratch checkout + settings.json only.
- **Arm 2 — +agent:** the canonical `backend` specialist from this repo.
  `scripts/install.sh` is run in this clone; its generated
  `.claude/agents/backend.md` is copied into the scratch checkout's
  `.claude/agents/`; the run adds `--agent backend`.
- **Arm 3 — +orientation:** scratch checkout + settings.json + a
  `CLAUDE.md` at the checkout root containing the frozen Orientation
  text (appendix below). No specialist agent.
- **Arm 4 — Copilot base (secondary):** Copilot CLI 1.0.89, BYOK
  Anthropic with the same model id, env per the W3 brief,
  `COPILOT_ALLOW_ALL=true`, `copilot -p '<prompt>'`, scratch checkout +
  no additions. Tasks T1 and T3 only, run only if budget remains after
  all Claude arms. Copilot output is graded from disk only; its
  self-report is ignored.

Deviation from the brief's suggested arm 3, decided pre-run: the
canonical skills (session-harden, wiki-lint) and the other canonical
agents (data-scientist, ux-ui) are off-domain for foreign-codebase
bugfixing; an off-domain specialist arm would be padding. Orientation
is the meaningful third treatment and matches the brief's
"+skill/orientation" arm label. NetworkX's own `AGENTS.md` exists only
at T1's parent and is contribution policy, not code orientation; arm 1
is "repo as-is" there, as everywhere.

## Metrics and grading

- Per run: success (binary, primary), `num_turns` and `total_cost_usd`
  from the Claude JSON envelope (Copilot: token counts from its output,
  converted at $1/M input, $5/M output), wall seconds.
- Grading, by the evaluator after the agent exits, never from agent
  self-report: copy the real commit's version of the changed test
  file(s) over the run tree, run the task's grading test node IDs with
  the pinned venv, success = every grading test passes.
- Also recorded per run: `git diff --stat` of the run tree and a 1–3
  line failure note when success = no.

## Claims and thresholds (n=4 tasks; descriptive, not powered)

- Claim A "specialist agent improves success on real code":
  PROVEN if arm 2 solves ≥1 task arm 1 fails AND arm 2 solves ≥ as
  many tasks overall as arm 1. REFUTED if arm 2 solves fewer tasks
  than arm 1. Otherwise UNVERIFIABLE (equal totals, no discordant
  pair, or incomplete runs).
- Claim B "orientation improves success on real code": same rule,
  arm 3 vs arm 1.
- Cost/turn comparisons reported as raw totals per arm; no threshold.

## Budget and stop rules

- Hard cap: $9.00 total Anthropic spend across all runs in this
  workstream. Cumulative cost logged in the results file after each run.
- Single-run soft cap ~$1.50: a run passing it is killed and logged.
- Shrink order if budget or the 13:30 ET initial-results deadline
  squeezes: drop arm 3 for remaining tasks, then arm 4, then T4.
  Minimum viable: 3 tasks × arms 1–2. Rigor (fresh tree per run,
  disk-based grading, identical prompts) is never shrunk.

## Appendix — Orientation text (frozen; arm 3 `CLAUDE.md`, verbatim)

```markdown
# NetworkX — orientation

NetworkX is a Python library for creating, manipulating, and studying
graphs. Package code lives in `networkx/`; import it as
`import networkx as nx`.

## Layout

- `networkx/classes/` — the graph classes (Graph, DiGraph, MultiGraph,
  MultiDiGraph) and their views/filters.
- `networkx/algorithms/` — algorithm subsystems, one package per area
  (centrality, isomorphism, tree, connectivity, ...). Most public
  functions are re-exported through the subsystem `__init__.py` and
  ultimately through `networkx/__init__.py`.
- `networkx/generators/` — graph generators (classic, lattice,
  community, ...).
- `networkx/utils/` — shared machinery: `decorators.py` (argmap,
  not_implemented_for, open_file), `misc.py`, backend dispatch.
- `networkx/readwrite/`, `networkx/drawing/`, `networkx/convert.py` —
  IO, layouts, conversion.
- Tests are colocated: each subsystem has a `tests/` directory next to
  the modules it tests. `networkx/conftest.py` holds shared fixtures.

## Conventions

- Public functions carry numpydoc docstrings, usually with runnable
  examples; keep them accurate when you change behavior.
- User-facing errors use networkx exceptions: `nx.NetworkXError`,
  `nx.NetworkXPointlessConcept`, `nx.NetworkXNoPath`, etc.
- Many public functions are wrapped with decorators from
  `networkx.utils.decorators` (e.g. `@not_implemented_for("directed")`,
  `@nx._dispatchable`). Preserve the wrappers and `__all__` entries.
- Functions that take a `seed` argument use the `np_random` decorator
  pattern; generators return `nx.Graph` objects and honor `seed` for
  reproducibility.
- Match the local style of the file you are editing; the project lints
  with ruff.

## Working

- Run tests targeted, never the whole suite:
  `/home/hatch/workspace/p2/w3/scratch/venv/bin/python -m pytest <path> -q`
  from the repo root. That interpreter has pytest, numpy, and scipy.
- A failing test in the same `tests/` directory as the module you are
  changing is the first thing to explain; a green targeted file is the
  minimum bar before you call a fix done.
- Optional dependencies (pandas, matplotlib, ...) are not installed;
  code paths needing them are skipped in tests and are usually not
  where a core bug lives.
```
