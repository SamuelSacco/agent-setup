# X3 Screening — Pre-registration

Date: 2026-10-01. Committed before any screening run.
Wave: C-C (screening only — the A/B itself is a follow-on wave).
Branch: `lab/x3-screening`, off master `e181f61`.

## Question

Ledger S16 / backlog X3: "Orientation improves Copilot CLI success on
real code" is UNVERIFIABLE — Copilot base is 3/3 on every task it has
run (T1, T3, R2; `evals/results/2026-09-30-P2-copilot-ab.md`). On
ceiling tasks an orientation win is structurally impossible. This wave
constructs a harder task band on which Copilot base demonstrably
fails, so the follow-on A/B has headroom to measure.

## Task-mining criteria (fixed before mining)

- Real historical fix commits in real repos (NetworkX, Textualize/rich,
  pallets/click). No synthetic bugs, no invented tasks.
- The fix commit must carry test changes usable as an oracle: grading
  overlays the fix commit's test files onto the run tree and executes
  the named pytest nodes (the packaged-runner protocol,
  `scripts/run_eval.py`).
- Oracle must discriminate, verified on disk before a candidate is
  accepted: grading nodes FAIL at the parent commit (with only the
  fix's test files applied) and PASS at the fix commit.
- Harder than the T1–T4 / U1–U4 band by mechanism, not adjectives:
  multi-hunk or multi-file fixes, subtle invariants, symptom far from
  cause, or an obvious-looking fix that is wrong. One-line typo/rename
  fixes and pure test changes are excluded.
- Recent (2024–2025) fixes preferred, to reduce memorization risk.
- Prompts are symptom-only, in the packaged house style: they never
  name the fix, the fix commit, or the root cause.
- Target: 8–10 accepted candidates entering screening.

## Screening protocol (fixed before any run)

- Tool: Copilot CLI (version recorded in the results file; 1.0.90 at
  prereg time), BYOK Anthropic, model `claude-haiku-4-5-20251001` —
  same model, prompts, isolation, and disk grading as the S16 arms.
- Arm: base only (no orientation file, no agent). Pre-approved mode
  (`COPILOT_ALLOW_ALL=true`, set by the runner).
- Cost accounting: the W3/P2 convention — footer token totals at
  $1/M input, $5/M output. This counts cached input at full rate and
  is an upper bound, never a billed figure. All caps below are on
  this converted figure.
- **Spend cap: $8.00 converted for the entire screening wave, hard
  stop.** Start-gate: a run is launched only if cumulative converted
  spend + $1.80 (the maximum observed Copilot base-run cost in this
  project) stays ≤ $8.00. A run that crosses the cap mid-flight is
  the last run; the overshoot, if any, is recorded, not smoothed.
- Stage 1: 2 base attempts per candidate, in candidate order.
- Stage 2: candidates with ≥1 FAIL in stage 1 receive attempts 3–4,
  ordered by stage-1 failure count (2-fail candidates first), under
  the same start-gate, until the cap binds.
- Harness ERROR verdicts do not count as attempts; one retry is
  permitted per errored run, budget permitting.
- **Band membership: a candidate enters the band iff Copilot base
  FAILs ≥2 of its attempts (of up to 4), disk-graded.** Candidates
  passing 2/2 in stage 1 are recorded as screened-out (no failure
  signal observed); no claim is made that they could never fail.
- Target outcome: ≥4 band tasks. If the cap binds before stage 1
  completes, or fewer than 4 candidates qualify, the wave reports
  exactly that — the band could not be constructed at this budget —
  with the per-candidate tallies as the evidence.

## Dated amendment — candidate list (2026-10-01 04:55 UTC, before any screening run)

Mining workers delivered 5 candidates with disk-verified discriminating
oracles (verification logs in ~/workspace/x3-mining/{a,b}/
verification.md; all 5 packages committed here under
evals/tasks-packaged/):

| # | id | repo | fix commit | grading nodes |
|---|---|------|------------|---------------|
| 1 | rich-u5-split-cells-double-width | Textualize/rich | babf74a7 | test_split_cells_mixed (5 params) |
| 2 | rich-u6-panel-title-background | Textualize/rich | 30e5ed61 | test_title_text_with_panel_background |
| 3 | rich-u7-wrap-double-width | Textualize/rich | 59b1aca6 | test_chop_cells, test_chop_cells_double_width_boundary, test_chop_cells_mixed_width, test_wrap_cjk_mixed |
| 4 | click-c1-flag-value-optional | pallets/click | 91de59c6 | test_flag_value_optional_behavior, test_flag_value_with_type_conversion |
| 5 | click-c2-help-option-eagerness | pallets/click | 70c673d3 | test_help_param_priority |

4 more NetworkX candidates (nx-t5..nx-t8) are being mined; they enter
stage 1 in the same order when delivered. No screening runs have
executed; the protocol above is unchanged.

## Dated amendment 2 — NetworkX candidates (2026-10-01 05:00 UTC, before any NetworkX screening run)

| # | id | repo | fix commit | grading nodes |
|---|---|------|------------|---------------|
| 6 | nx-t5-betweenness-k-scaling | networkx/networkx | a802a27f | TestEdgeBetweennessCentrality::test_edge_betweenness_k (discriminating), test_equivalence_non_subset (regression guard, passes at parent) |
| 7 | nx-t6-is-aperiodic-strong-connectivity | networkx/networkx | 86e143dd | 6 test_is_aperiodic_* nodes |
| 8 | nx-t7-network-simplex-faux-inf | networkx/networkx | 7768b927 | test_network_simplex_large_capacities (8 params), test_network_simplex_unbounded_flow |
| 9 | nx-t8-diameter-usebounds-weighted | networkx/networkx | c732e434 | TestDistance::test_use_bounds_on_off_consistency (500 params) |

All 4 oracles verified discriminating on disk by the mining worker
(parent FAIL → fix PASS; details in ~/workspace/x3-mining/a/
verification.md). Candidate pool is now 9 (target 8-10 met).
Scheduling note: rich/click stage-1 runs were allocated sub-caps
summing to the $8 wave cap; NetworkX stage-1 runs launch afterwards
under the same global cap and start-gate, in candidate order, with
whatever budget remains — if the remainder cannot clear the start
gate, the nx candidates are recorded as mined-but-unscreened and the
band verdict rests on the screened pool.

## Follow-on A/B protocol (registered now, executed by a later wave)

- 4 band tasks × 2 arms (base vs +orientation), same runner, model,
  and grading as S16. Orientation arm = `--arm orient` with the
  repo's existing orientation fixture for the task's repo
  (`evals/fixtures/networkx-orientation.md` /
  `evals/fixtures/rich-orientation.md`; a click fixture in the same
  format must be written and committed before any click A/B run).
- Pair = both arms of one task. A pair counts only when both arms
  complete with disk grades.
- Decision rule (the S16 Claim C rule): PROVEN if ≥1 discordant pair
  favors +orientation and no discordant pair favors base; REFUTED if
  base solves more tasks than +orientation across completed pairs;
  otherwise UNVERIFIABLE. Incomplete pairs are excluded from the
  tally and reported as incomplete.
- A/B spend ceiling: $18 converted (backlog estimate $10–18), with a
  start-gate: a pair is started only if projected spend for both arms
  at $2.20/run keeps cumulative ≤ ceiling.

## What this wave does not do

- No orientation arm runs. No A/B. No master merge (driver merges
  after verification). No claim about S16 changes until the follow-on
  A/B completes: screening results update backlog X3's status and the
  S16 ledger entry records the band construction only.
