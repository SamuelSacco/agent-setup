# P2 Copilot Orientation A/B — Results

Date: 2026-09-30. Pre-registration:
`evals/results/2026-09-30-P2-copilot-ab-prereg.md` (commit `b4bde7d`,
pushed before any run). Raw numbers and verdicts only.

Question: does the orientation effect measured on Claude (combined
n=8: orientation 8/8 vs base 6/8) also appear in Copilot CLI?
Tool: Copilot CLI 1.0.89, BYOK Anthropic, model
`claude-haiku-4-5-20251001` — same model, prompts, isolation, and
disk grading as the Claude arms. Success = every grading test from
the real fix commit passes when overlaid on the run tree and run by
the evaluator (never agent self-report).

## What ran

The budget bound this hard. Copilot's converted cost per run is
3–9× Claude's on identical tasks (T1 +orient: 2.0M input tokens vs
~200–400k for a Claude run), so the $4 cap bought 3 new runs, not 14.
The preregistered start-gate ($3.40) stopped the rest; the final R2
base run started under the gate and cost $1.80, landing total new
spend at $4.63 against the ~$4 cap — the overshoot is one run's cost,
recorded here rather than smoothed over.

| Task | Arm | Success | Cost USD (converted) | Wall s | Grading tests |
|------|-----|---------|---------------------|--------|---------------|
| T1 ISMAGS | base (W3, reused) | **yes** | ~1.49 | 198 | 3 passed |
| T1 | +orientation | **yes** | 2.19 | 483 | 3 passed |
| T3 current_flow | base (W3, reused) | **yes** | ~0.47 | 97 | 4 passed |
| T3 | +orientation | **yes** | 0.63 | 130 | 4 passed |
| R2 eccentricity null graph | base | **yes** | 1.80 | 211 | 2 passed |
| R2 | +orientation | — not run (budget gate) | | | |
| R1, R3, T2, R4, T4 | both arms | — not run (budget gate) | | | |

New-run totals: 3 runs, all passed, $4.63 converted. Reused W3 base
runs: T1/T3, both passed, ~$1.96 converted (not counted against this
workstream's cap; same protocol, see prereg).

\* Conversion is the W3 convention: footer token totals at $1/M input,
$5/M output. Footers are rounded, and nearly all input tokens were
cached (T1 +orient: 2.0M of 2.0M) yet are counted at the full input
rate — converted figures are upper-bound estimates, kept identical to
W3 for comparability, not billed amounts.

## Verdict (pre-registered Claim C rule)

**Claim C — "orientation improves Copilot success on real code":
UNVERIFIABLE.** Completed pairs: 2 of 8 (T1, T3). Both are concordant
passes — base 2/2, +orientation 2/2, no discordant pair in either
direction. The rule requires ≥1 discordant win for PROVEN and fewer
solves for REFUTED; neither fired. The remaining 6 pairs are
incomplete and excluded from the tally, per the prereg.

Why there was no headroom in the completed pairs: Copilot base has
not failed any task it has run in this project — 3/3 here (T1, T3,
R2), including R2, the task whose Claude base run failed (on
exception-message wording; Copilot's base fix passed both tests). On
tasks where the base arm is already at ceiling, an orientation win is
structurally impossible; the two Claude discordant pairs (T1, R2)
were both tasks Copilot base solves unaided. Whether orientation
helps Copilot on tasks its base arm fails remains untested — no such
task was observed within budget.

Descriptive facts, for the record:
- +orientation cost more than base on both completed pairs
  (T1: $2.19 vs ~$1.49; T3: $0.63 vs ~$0.47) and was slower
  (483s vs 198s; 130s vs 97s) — the opposite cost direction from the
  Claude arms, where orientation was the cheapest arm overall.
  n=2 pairs; no threshold was pre-registered for cost.
- All three new runs produced real, minimal fixes in their assigned
  trees (T1 +orient: ismags.py, +4/−1; T3 +orient:
  current_flow_closeness.py, +4/−0; R2 base: distance_measures.py,
  +4/−0). No fabrication, no tree escapes; the mining clone's
  cleanliness assert was green before every setup and after every run.

## Deviations and incidents (complete list)

1. **Budget truncation.** 11 of 14 planned new runs were skipped by
   the preregistered budget gate after Copilot's per-run token volume
   (1.7–2.0M input tokens on T1/R2) priced the full matrix at roughly
   $15–25 converted — 4–6× the cap. The verdict above is therefore a
   statement about 2 completed pairs, not about the 8-task design.
2. **Cap overshoot $0.63.** The start-gate admits a run at ≤$3.40
   cumulative; the R2 base run admitted at $2.83 cost $1.80. Total
   $4.63 vs the ~$4 cap. No further runs were started after the gate
   tripped.
3. **Time-gate fix, pre-run.** The runner's first invocation refused
   to run: the VM clock is UTC and the 12:55 gate was compared in
   local time (15:15 UTC). Fixed to America/New_York before any run
   executed; no run was affected.
4. No trust-gating incident: `COPILOT_ALLOW_ALL=true` runs edited
   their scratch checkouts without prompts, as in W3.
5. Runner, raw outputs, per-run diffs, and the spend ledger are
   preserved in `~/workspace/p2/copilot-ab/` (`runner.py`, `runs/`,
   `ledger.tsv`).
