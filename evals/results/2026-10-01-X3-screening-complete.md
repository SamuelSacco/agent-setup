# X3 Screening — Completion Attempt (Wave 6)

Date: 2026-10-01. Wave: 6 (overnight token-max fleet), continuing
branch `lab/x3-screening` @ d8bad67. Protocol: the pre-registration in
`evals/results/2026-10-01-X3-screening-prereg.md`, as executed by
waves 1 and 4-A (stage 1 = 2 base attempts per candidate; stage 2 =
attempts 3–4 for candidates with ≥1 stage-1 FAIL; band membership =
base FAILs ≥2 of up to 4 attempts, disk-graded; harness ERRORs do
not count as attempts). Fresh cap for this wave, decided by main
chat: screening completion $30 converted; the pre-registered A/B
($18 ceiling) pre-authorized contingent on final band ≥ 4.
Candidates remaining at wave start: nx-t7, nx-t8, rich-u6, rich-u7.
Tool: Copilot CLI 1.0.90, BYOK Anthropic,
model `claude-haiku-4-5-20251001`, base arm only.

## Verdict

**The screen could not be completed: the Anthropic API credit
balance behind the Copilot BYOK key was exhausted before this wave's
first launch, and every launch in the wave was refused before any
model work occurred. All four remaining candidates stay UNSCREENED.
Band = 1 member (click-c2, wave 4-A) < 4, so the pre-registered A/B
did not run. X3 / ledger S16 remains UNVERIFIABLE — now with 5 of 9
candidates resolved and the remaining 4 blocked on an account
funding action, not on protocol or budget.**

## Coordinator ruling — the wave's FAIL verdicts are not attempts

Each of the 8 worker launches (2 per candidate, detached per the
wave-4-A SIGTERM finding) plus 1 coordinator probe launch ended the
same way, disk-verified in every run dir's `raw-output.txt`:

```
400 Your credit balance is too low to access the Anthropic API.
Please go to Plans & Billing to upgrade or purchase credits.
Changes    +0 -0
```

- The agent never executed: zero file changes, zero tokens, no
  token footer in any `raw-output.txt` (so no converted cost exists
  to recompute).
- The runner recorded VERDICT: FAIL (exit 1) because grading the
  untouched parent tree fails the discriminating nodes — the same
  failure the oracle produces at the parent commit by design.
- Per the pre-registration, band membership requires disk-graded
  FAILs of the base arm. A refusal before the arm runs is an
  infrastructure ERROR (the class the protocol excludes from
  attempts), not a base failure. Counting these would place nx-t7,
  nx-t8, rich-u6, and rich-u7 in the band on zero model evidence —
  the opposite of what the band exists to prove.
- Window: launches at 06:10–06:23 UTC all refused; the coordinator
  probe at 06:25 UTC (02:25 ET) was refused identically, so the
  exhaustion persisted for the whole wave. Fleet context: metered
  API work succeeded as late as ~01:55 ET (X21) and wave 4-A
  screening ran normally at 01:20–01:39 ET; the balance hit zero
  between those points.

## Full 9-candidate screen table (all waves)

| candidate | attempts (valid) | results | status |
|---|---|---|---|
| rich-u5-split-cells-double-width | 2 (wave 1) | PASS, PASS | screened **out** |
| click-c1-flag-value-optional | 2 (wave 4-A) | PASS, PASS (`PYTHONPATH=src`) | screened **out** |
| click-c2-help-option-eagerness | 2 (wave 4-A) | FAIL, FAIL (`test_help_param_priority`) | **IN BAND** |
| nx-t5-betweenness-k-scaling | 2 (wave 4-A) | PASS, PASS | screened **out** |
| nx-t6-is-aperiodic-strong-connectivity | 2 (wave 4-A) | PASS, PASS (6/6 nodes) | screened **out** |
| nx-t7-network-simplex-faux-inf | 0 — 2 launches refused (API credit 400) | — | UNSCREENED (credit) |
| nx-t8-diameter-usebounds-weighted | 0 — 2 launches refused (API credit 400); 1 additional launch lost to a network clone ERROR, retried per protocol | — | UNSCREENED (credit) |
| rich-u6-panel-title-background | 0 — 2 launches refused + 1 coordinator probe refused (API credit 400) | — | UNSCREENED (credit) |
| rich-u7-wrap-double-width | 0 — 2 launches refused (API credit 400) | — | UNSCREENED (credit) |

Per-launch evidence: `evals/results/2026-10-01-RUN-<id>-copilot-base-attempt<N>.md`
for all 8 worker launches (RUN files state Cost USD: None, diff
+0 −0 — read them together with this ruling, not as grades), and
`2026-10-01-RUN-rich-u6-panel-title-background-copilot-base-coordinator-probe.md`
for the probe. Raw outputs remain in the worker clones
(`~/workspace/w6-nx-t7`, `w6-nx-t8`, `w6-rich-u6`, `w6-rich-u7`
under `evals/scratch-run-eval/runs/`).

## S16 verdict wording (as entered in the claims ledger)

Update 2026-10-01 (Wave 6 screening completion): stage 1 attempted
for the last 4 candidates (nx-t7, nx-t8, rich-u6, rich-u7) under a
fresh $30 cap — all 9 launches (8 worker + 1 coordinator probe,
06:10–06:25 UTC) were refused pre-execution with Anthropic API
`400 credit balance too low`; zero model work, zero tokens, recorded
as infrastructure ERRORs, not attempts. Screen therefore stands at
5 of 9 resolved (rich-u5, click-c1, nx-t5, nx-t6 out; click-c2 the
sole band member). Band 1 < 4: the pre-registered A/B did not run.
S16 stays UNVERIFIABLE, with the complete evidence base; the blocker
is now Samuel's Anthropic API credit, not budget authorization or
protocol. On credit restoration, the remaining step is mechanical:
stage 1 for the 4 unscreened candidates under a fresh ~$25 cap at
the wave-4-A corrected calibration (~$3/run nx/rich, ~$4.50
click-class), then the A/B iff the band reaches 4.

## Spend accounting

- **Screening completion: $0 recorded of the $30 cap.** Every launch
  was refused before token consumption; no `raw-output.txt` in the
  wave contains a token footer, so there is nothing to convert.
  (The API may meter refused calls at $0; no figure is claimed
  beyond "no footer, no tokens".)
- A/B: $0 of $18 (did not trigger; band < 4, and no credit to run
  it with in any case).
- Prior X3 spend stands as recorded: wave 1 $6.99 of $8;
  wave 4-A $24.9025 of $25.

## What remains, and what unblocks it

1. **Samuel restores Anthropic API credit** (Plans & Billing on the
   account behind the Copilot BYOK key / `custom.anthropic`
   connector). No fleet action can substitute for this.
2. Re-run stage 1 for nx-t7, nx-t8, rich-u6, rich-u7 (fresh ~$25
   cap, corrected calibration). Stage 2 only for a 1-FAIL split.
3. If the final band reaches ≥ 4, run the pre-registered A/B
   exactly as specified in the preregistration (4 band tasks × 2
   arms, discordant-pair rule, $18 ceiling; the click orientation
   fixture must be written and committed before any click A/B run,
   since click-c2 is a band member).
