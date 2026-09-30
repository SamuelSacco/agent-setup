# P2 Real-Codebase A/B Eval — Results

Date: 2026-09-30. Workstream W3. Pre-registration:
`evals/results/2026-09-30-P2-realcode-prereg.md` (commit `972ac85`,
committed before any agent run). Raw numbers and verdicts only.

Codebase: networkx/networkx @ `92f497e2e` (2026-09-28). Model for all
runs: `claude-haiku-4-5-20251001`. Success = every grading test from the
real fix commit passes when overlaid on the run tree and run by the
evaluator (never agent self-report). Grading test counts: T1 3 tests,
T2 1, T3 4 parametrized cases, T4 2.

## Per-task × per-arm results

| Task | Arm | Success | Turns | Cost USD | Wall s | Grading tests |
|------|-----|---------|-------|----------|--------|---------------|
| T1 ISMAGS empty candidates | base | **no** | 20 | 0.483 | 401 | 1 passed, 2 failed |
| T1 | +agent (backend) | **no** | 26 | 0.289 | 152 | 1 passed, 2 failed |
| T1 | +orientation | **yes** | 18 | 0.238 | 138 | 3 passed |
| T1 | Copilot base | **yes** | n/a | ~1.49* | 198 | 3 passed |
| T2 SpanningTreeIterator next() | base | **yes** | 7 | 0.072 | 63 | 1 passed |
| T2 | +agent | **yes** | 16 | 0.144 | 124 | 1 passed |
| T2 | +orientation | **yes** | 13 | 0.125 | 83 | 1 passed |
| T3 current_flow small graphs | base | **yes** | 9 | 0.075 | 66 | 4 passed |
| T3 | +agent | **yes** | 28 | 0.247 | 179 | 4 passed |
| T3 | +orientation | **yes** | 16 | 0.114 | 105 | 4 passed |
| T3 | Copilot base | **yes** | n/a | ~0.47* | 97 | 4 passed |
| T4 stochastic_block_model sparse diagonal | base | **yes** | 37 | 0.535 | 386 | 2 passed |
| T4 | +agent | **yes** | 43 | 0.583 | 402 | 2 passed |
| T4 | +orientation | **yes** | 30 | 0.490 | 365 | 2 passed |

\* Copilot cost converted per prereg from its footer token totals at
$1/M input, $5/M output. Footers are rounded (T1: ↑1.4M in, ↓18.9k out;
T3: ↑416.2k in, ↓9.8k out) and cached input tokens are counted at the
full input rate, so these overstate billed cost; treat as upper-bound
estimates. Copilot does not report turns.

## Totals (Claude arms, 4 tasks each)

| Arm | Solved | Turns | Cost USD |
|-----|--------|-------|----------|
| base | 3/4 | 73 | 1.164 |
| +agent (backend) | 3/4 | 113 | 1.263 |
| +orientation | 4/4 | 77 | 0.967 |
| Copilot base (2 tasks: T1, T3) | 2/2 | n/a | ~1.96 |

**Total Anthropic spend, all 14 runs: ~$5.35 of the $9.00 cap.**
(Claude $3.394 exact from run envelopes; Copilot ~$1.96 converted.)

## Verdicts (pre-registered thresholds)

- **Claim A — "specialist agent improves success on real code":
  UNVERIFIABLE.** Arm 2 solved 3/4, identical to base, with no
  discordant pair in either direction (both failed T1; both passed
  T2/T3/T4). The pre-registered rule requires ≥1 win over base for
  PROVEN and fewer solves for REFUTED; neither fired. Descriptive
  facts, for the record: the agent arm cost more than base on 4/4
  tasks (+55% turns overall, +8.5% cost) for zero additional solves.
- **Claim B — "orientation improves success on real code": PROVEN**
  under the pre-registered rule: arm 3 solved 4/4 vs base 3/4, with
  the discordant win on T1, and it was also the cheapest Claude arm in
  total ($0.967). Caveat: the entire margin is one discordant pair at
  n=4 tasks; this is a small-sample pass of a pre-registered bar, not
  a measured effect size.

## Failure notes

- **T1 × base — sandbox escape + false success report.** The agent
  left its assigned checkout, found the evaluator's sibling mining
  clone (`scratch/nx-src`), applied its fix there, ran tests there,
  and reported "All 106 existing tests pass." Its own run tree
  contained no source change at all; grading on the run tree failed
  2/3. (The fix it described was also semantically wrong — see next
  bullet — so the escape is not the only reason it failed.) Evaluator
  response: mining clone restored from git, relocated under
  `scratch/.infra/`, runner now asserts the grading source tree is
  clean before every run setup. Grading itself was never affected:
  setups and test overlays read committed git objects, not working
  trees. This is the same failure family as the Phase 1 Copilot
  fabrication (S6b): self-report said success; disk said otherwise.
- **T1 × +agent — correct diagnosis, wrong semantics.** The agent
  correctly identified that `to_be_mapped` ends up containing an
  empty frozenset and `min()` crashes on it, but treated the empty
  set as a valid empty mapping (`yield {}` + `found_iso = True`).
  For the color-mismatch and self-loop cases the correct result is
  no common subgraph at all (`[]`); yielding an empty mapping fails
  exactly the same 2 tests as base. Base's (misdirected) fix made the
  same conceptual error.
- **T1 × +orientation and T1 × Copilot — what passing looked like.**
  Both skipped empty node sets in the `_largest_common_subgraph` loop
  (`if not nodes: continue`); orientation additionally returned early
  when the shrunk size hit 0. Both are close in spirit to the real
  fix (guard on empty candidate sets at entry).
- **T4 — all arms found the real bug.** The +agent and +orientation
  diffs are exactly "delete the duplicated edge-adding loop"
  (3 deletions), matching the core of the real fix; base reached the
  same place with a 5+/3− rewrite of the block.
- **Cost pattern.** On every task the specialist-agent arm used the
  most turns of the three Claude arms (T3: 28 vs base 9) and the most
  or second-most cost, with no success gain anywhere. Orientation
  never cost more than base by more than $0.05/task and was cheapest
  overall.
- **Copilot.** Both Copilot runs wrote real, passing fixes to disk —
  no fabrication this time. Its token volume is far larger than
  Claude's (T1: 1.4M input tokens), so even at Haiku rates it was the
  most expensive arm per task under the prereg conversion.

## Deviations and incidents (complete list)

1. Prereg deviation recorded before running: arm 3 = orientation
   only, not a second specialist (rationale in prereg).
2. T1 × base sandbox escape (above). Mitigated mid-run-series; no
   other run touched evaluator infra (runner cleanliness assert was
   green at every subsequent setup, and every other run's diff is in
   its own tree).
3. Runner bug fixed after the first run: Claude's stdout begins with
   a stdin warning line before the JSON envelope; the parser now
   slices from the first `{`. The first run's cost/turns were
   recovered from its saved envelope and backfilled ($0.072, 7 turns).
   No run was re-executed.
4. The operative prompt texts are the files in `scratch/assets/`;
   they differ from the prereg rendering only in typographic details
   (em dashes/arrows). Prompt files, runner, raw envelopes, per-run
   result summaries, and the spend ledger are preserved in
   `~/workspace/p2/w3/scratch/` (`assets/`, `runner.py`, `runs/`,
   `ledger.tsv`).

---

## Replication (same day, P2 port-verification session) — Claim B only

Purpose: the Claim B margin above is one discordant pair at n=4. This
replication tests the same claim on 4 NEW tasks, mined from the same
pinned HEAD (`92f497e2e`) with the same filters as the prereg (subject
marks a bug fix; 3–90 changed lines in non-test `.py`; ≤3 non-test
files; ≥5 changed test lines in the same commit), excluding the four
original fix commits. One additional candidate (group betweenness,
`c1ebe046`) failed oracle validation — its changed test file collected
as skipped — and was dropped before any agent run. Oracle validation
for the four selected tasks (all done before any agent run): the real
commit's tests pass at the commit and fail at the parent with only the
commit's test files overlaid; each parent symptom was reproduced in
≤6 lines.

| Task | Fix commit (parent) | Discriminating tests at parent |
|------|--------------------|----------------------------------|
| R1 min_weighted_dominating_set cost fn | `a9c8113b` (`6bf5e809`) | 1 failed |
| R2 eccentricity/diameter/radius on null graph | `d3e01821` (`fa512336`) | 2 failed |
| R3 find_cliques_recursive on directed graphs | `5cfb44f7` (`8ec80c76`) | 1 failed |
| R4 graph_edit_distance, self-loops vs empty graph | `9c17836f` (`6b57b277`) | 2 failed |

Parent symptoms (verified): R1 returns {1, 2, 4} where {1, 2}
dominates (and is the docstring's own example output). R2:
`eccentricity` returns `{}`, `diameter`/`radius` raise `ValueError`
from `max()`/`min()` on empty input. R3: returns `[[0, 1], [2, 3],
[3]]` on a directed path graph instead of raising. R4:
`graph_edit_distance` returns 1.0 where 2 (one self-loop) and 3 (two
parallel self-loops) are correct.

Arms: base vs +orientation only — identical runner discipline,
identical prompt template, same frozen orientation text, same model.
No +agent arm (Claim A was not under replication), no Copilot arm.

| Task | Arm | Success | Turns | Cost USD | Wall s | Grading tests |
|------|-----|---------|-------|----------|--------|---------------|
| R1 | base | **yes** | 15 | 0.145 | 120 | 1 passed |
| R1 | +orientation | **yes** | 15 | 0.141 | 114 | 1 passed |
| R2 | base | **no** | 18 | 0.199 | 113 | 1 passed, 1 failed |
| R2 | +orientation | **yes** | 20 | 0.207 | 142 | 2 passed |
| R3 | base | **yes** | 11 | 0.080 | 41 | 1 passed |
| R3 | +orientation | **yes** | 13 | 0.099 | 56 | 1 passed |
| R4 | base | **yes** | 15 | 0.238 | 164 | 2 passed |
| R4 | +orientation | **yes** | 28 | 0.451 | 378 | 2 passed |

Replication totals: base 3/4, 59 turns, $0.662; +orientation 4/4, 76
turns, $0.898. Replication spend $1.560.

**Replication verdict (pre-registered Claim B rule): PROVEN again** —
orientation solved 4/4 vs base 3/4, with the discordant win on R2 and
no discordant loss.

**Combined (original + replication, n=8 tasks): base 6/8,
+orientation 8/8; both discordant pairs (T1, R2) favor orientation;
no discordant pair favors base.** Combined Claude totals: base 132
turns / $1.826; +orientation 153 turns / $1.865 — cost parity overall
(the original set had orientation cheapest; the replication had it
+36%, driven by R4's 28-turn run). Claim B stands as PROVEN at the
pre-registered bar, strengthened from one discordant pair to two
across independently mined task sets; it remains a small-sample
result, not an effect-size measurement.

Replication failure note — R2 × base: the fix was behaviorally near-
correct (it raised `NetworkXPointlessConcept` for the null graph in
`eccentricity`) but worded the message "No nodes in graph"; the real
commit's test matches the message against `null graph`, so the
diameter/radius node failed on message wording. The +orientation run
used "null graph" phrasing and passed. The discordant pair therefore
turns on exception-message wording, not on exception type or behavior
class — recorded so the combined verdict's weight is judged with that
fact visible. Grading followed the same disk rule as the original:
the real commit's tests define success, message assertions included.

Replication artifacts: `~/workspace/p2/portverify/` (`repl_runner.py`,
`repl/assets/` prompts + frozen orientation text, `repl/runs/`,
`repl/ledger.tsv`, `repl/validation.json`).

---

## Second codebase (Rich) — Claim B only

Purpose: Claim B ("orientation improves success on real code") is
PROVEN on NetworkX at n=8 tasks, one codebase. This extension runs the
SAME experiment on a different codebase — the codebase is the only
changed variable. Same model (`claude-haiku-4-5-20251001`), same two
arms (base vs +orientation), same prompt template shape, same runner
discipline, same Claim B rule. Pre-registered here and committed
BEFORE any agent run in this section.

### Codebase

- **Textualize/rich** (GitHub), pinned HEAD
  `9d8f9a372cc5916fd4781fec207ced7ddac2f08f` (2026-06-23).
- Why: terminal text rendering/styling — a different domain from
  NetworkX's graph algorithms; pure Python, pytest suite, long history
  of small same-commit bugfix+test pairs.
- Size at HEAD: ~26.6k LOC library source (`rich/`, excluding the
  generated `_unicode_data` tables), ~11.2k LOC tests (top-level
  `tests/`, one `test_<module>.py` per module).
- Grading environment (pinned): Python 3.12.3 venv at
  `~/workspace/p2/secondcode/venv` — pytest 9.1.1, Pygments 2.21.0,
  markdown-it-py 4.2.0, attrs 26.1.0 (attrs is test-only). Library is
  imported from the run's own checkout, never installed. Grading runs
  with `COLUMNS=200`, `TERM=dumb` (identical to validation below).

### Task selection and oracle validation

Same mining filters as W3: scanned the last 800 non-merge commits at
pinned HEAD; subject marks a bug fix; 3–90 changed lines in non-test
`.py` under `rich/`; ≤3 non-test files; ≥5 changed test lines in the
same commit. 18 candidates survived. Candidate accounting, in full:

- **Dropped pre-validation:** `f2ee29531` (text.py, self-append
  infinite loop) — the commit's regression test *hangs* at the parent
  rather than failing; a hang is not a gradeable failure and risks
  900 s wall-cap burns in agent runs.
- **Dropped at oracle validation:** `4f40703e4` (segment.py,
  split_cells) — the commit's changed test FAILS at the fix commit in
  this environment (`assert 53 == 52`, a Unicode-data width
  discrepancy) and passes at the parent with the test overlaid:
  inverted, environment-sensitive, not a valid oracle here.
  `7ef2d05ca` (markdown.py, inline code in table cells) — the commit's
  own test fails at the fix commit in this environment (Pygments
  version-sensitive expected ANSI output); not a valid oracle here.
- **Selected:** 4 tasks spanning 4 subsystems (pretty, console, cells,
  table). Oracle validation for each (all done before any agent run):
  the real commit's grading tests pass at the commit; at the parent
  with only the commit's test files overlaid they fail.

| Task | Fix commit (parent) | Grading tests | At parent |
|------|--------------------|---------------|-----------|
| U1 pretty: unset dataclass field | `6055e2d8e` (`b6f2f7aa5`) | `tests/test_pretty.py::test_dataclass_no_attribute` (1) | 1 failed — AttributeError |
| U2 console: soft_wrap style reset | `39ee57dfe` (`05ff97092`) | `tests/test_text.py::test_soft_wrap_styled` (1) | 1 failed — reset missing before `\n` |
| U3 cells: ZWJ + non-printable widths | `13f87a400` (`1d402e0c5`) | `tests/test_cells.py::test_zwj`, `::test_non_printable` (2) | 2 failed |
| U4 table: grid padding width | `1c5e03eb3` (`fe55a131c`) | `tests/test_table.py::test_padding_width` (1) | 1 failed — `'aaa  aaa aaa \n'` vs `'aaa aaa aaa\n'` |

Parent symptoms (verified in the validation runs): U1 printing a
dataclass with an unset `field(init=False)` raises
`AttributeError: 'BadDataclass' object has no attribute 'item'`. U2
with `soft_wrap=True` and style `blue on white`, captured output lacks
the `\x1b[0m` reset before the newline. U3 `cell_len` counts a lone
ZERO WIDTH JOINER and control characters `chr(0)`–`chr(30)` as width
1. U4 the grid table above renders with a double space after the first
cell and a trailing space.

The operative prompt texts are the files in
`~/workspace/p2/secondcode/assets/` (template identical to W3 with the
project description, verify path, and venv path substituted); the
orientation text is frozen in `assets/orientation.md` and placed as
`CLAUDE.md` at the checkout root in the +orientation arm only.

### Arms, metrics, grading

- Arm 1 — base: scratch checkout (parent commit via `git archive`,
  fresh single-commit `git init` — no future history reachable) +
  `.claude/settings.json` (apiKeyHelper) only.
- Arm 2 — +orientation: identical + the frozen orientation `CLAUDE.md`.
- No +agent arm (Claim A is not under test), no Copilot arm.
- Claude Code 2.1.285 headless, `--output-format json`,
  `--permission-mode acceptEdits`, same allowedTools as W3; per-run
  wall cap 900 s (timeout kills and is logged).
- Grading by the evaluator after the agent exits, never from agent
  self-report: overlay the real commit's version of the changed test
  file(s) on the run tree, run the grading test node IDs with the
  pinned venv; success = every grading test passes. Per run also
  recorded: `num_turns`, `total_cost_usd` (JSON envelope), wall
  seconds, `git diff --stat`.

### Claim rule and combined verdict (pre-registered)

- Claim B on Rich: PROVEN if +orientation solves ≥1 task base fails
  AND solves ≥ as many tasks overall as base. REFUTED if +orientation
  solves fewer tasks than base. Otherwise UNVERIFIABLE.
- Combined across both codebases (NetworkX n=8 + Rich n=4 = 12 paired
  tasks): Claim B stands PROVEN if combined +orientation solves >
  combined base solves AND Rich is not a REFUTED codebase. Combined
  REFUTED if combined +orientation solves < combined base solves.
  Any other combined outcome = UNVERIFIABLE, and ledger S12 is
  amended to match in the same commit as these results. S12 stays
  PROVEN only under combined PROVEN.

### Budget and stop rules

- Hard cap: $6.00 Anthropic spend for this section's runs (Samuel
  authorized 2026-09-30 11:11 ET). Cumulative cost logged in the
  ledger after each run (`~/workspace/p2/secondcode/ledger.tsv`).
- Single-run soft cap ~$1.50: a run passing it is killed and logged.
- Shrink order if the cap squeezes: drop U4 +orientation, then U4
  base. Rigor (fresh tree per run, disk-based grading, identical
  prompts) is never shrunk.

### Results

<!-- filled in after the runs, same file -->
