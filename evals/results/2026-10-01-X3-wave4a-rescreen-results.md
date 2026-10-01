# X3 Wave 4-A — Re-screening Results

Date: 2026-10-01. Wave: 4-A (overnight token-max fleet), continuing
branch `lab/x3-screening` @ da2fbce. Protocol: the pre-registration in
`evals/results/2026-10-01-X3-screening-prereg.md` (stage 1 = 2 base
attempts per candidate; stage 2 = attempts 3–4 for candidates with
≥1 stage-1 FAIL; band membership = base FAILs ≥2 of up to 4 attempts,
disk-graded). Fresh caps for this wave, decided by main chat after
the wave-1 cap accounting was poisoned: screening $25 converted;
the pre-registered A/B ($18 ceiling) pre-authorized contingent on
band ≥ 4. Candidate order per wave tasking: click-c1, click-c2,
nx-t5…t8, rich-u6, rich-u7 (rich-u5 already screened out in wave 1).
Tool: Copilot CLI 1.0.90, BYOK Anthropic,
model `claude-haiku-4-5-20251001`, base arm only,
`COPILOT_ALLOW_ALL=true` (runner-set). Click candidates run with
`PYTHONPATH=src` (the wave-1 §6 remedy).

## Verdict

**Band partially constructed: 1 member (click-c2). The A/B did not
run — the band is below the pre-registered minimum of 4 — and
X3 / ledger S16 remains UNVERIFIABLE.** The $25 screening cap bound
after stage 1 of 4 of the 7 remaining candidates. This is the
pre-registered outcome for a binding cap: report the tallies, do not
improvise a smaller band.

The wave did produce the first Copilot base failure signal of the
entire X3 effort: click-c2 failed 2/2 disk-graded attempts. Every
other screened candidate passed 2/2.

## Screening outcomes (all footer-verified on disk by the coordinator)

| candidate | attempts | results | converted cost | status |
|---|---|---|---|---|
| click-c1-flag-value-optional | 2 | PASS, PASS (2/2 nodes each) | $2.707 + $3.0485 = $5.7555 | screened **out** |
| click-c2-help-option-eagerness | 2 | FAIL, FAIL (`test_help_param_priority` both times) | $4.452 + $4.4375 = $8.8895 | **IN BAND** |
| nx-t5-betweenness-k-scaling | 2 | PASS, PASS (2/2 nodes each) | $1.918 + $3.0765 = $4.9945 | screened **out** |
| nx-t6-is-aperiodic-strong-connectivity | 2 | PASS, PASS (6/6 nodes each) | $2.6485 + $2.6145 = $5.2630 | screened **out** |
| nx-t7-network-simplex-faux-inf | 0 | — | — | UNSCREENED (cap) |
| nx-t8-diameter-usebounds-weighted | 0 | — | — | UNSCREENED (cap) |
| rich-u6-panel-title-background | 0 | — | — | UNSCREENED (cap) |
| rich-u7-wrap-double-width | 0 | — | — | UNSCREENED (cap) |

Stage 2: no candidate was eligible — no stage-1 outcome had exactly
1 FAIL (click-c2 reached 2 FAILs in stage 1 and is in the band by
the membership rule; attempts 3–4 would add no membership
information).

Per-attempt evidence: `evals/results/2026-10-01-RUN-<id>-copilot-base-attempt<N>.md`
in this branch; raw footers in each run dir's `raw-output.txt` under
the worker clones' `evals/scratch-run-eval/runs/` (worker clones:
`~/workspace/w4a-click-c1`, `w4a-click-c2`, `w4a-nx-t5`, `w4a-nx-t6`).

## Spend accounting

- **Verified total: $24.9025 of the $25.00 screening cap** — 8 graded
  attempts, every figure recomputed by the coordinator from the run
  dirs' `raw-output.txt` footers at the preregistered conversion
  ($1/M input, $5/M output; upper bound, cached input at full rate).
  Remaining headroom $0.0975: no further run clears any start-gate,
  so nx-t7, nx-t8, rich-u6, rich-u7 stay unscreened.
- Two launches were SIGTERM-killed before producing a footer or a
  results file and are excluded from every tally: click-c1's first
  launch (killed at 306s during source clone + venv bootstrap; the
  run dir holds partial agent work, so some model tokens may have
  been consumed — cost unknown, not zero) and nx-t5's first launch
  (killed at ~314s during the NetworkX source clone, before any tool
  tokens existed — $0). Cause: runs attached to a worker's exec
  session die with the session; all subsequent launches were
  detached (setsid/nohup) and completed. Process note, not a runner
  defect.

## Calibration finding — per-run cost was understated for click

Observed converted cost per graded run: $1.92–$4.45 (median ~$2.85).
click-c2 cost $4.45/run (↑4.3M input tokens per run vs 1.8–2.9M for
the other candidates); the wave-1 calibration (~$2.10 rich,
$2.82 click) and the preregistered A/B planning figure ($2.20/run)
understate this class by ~2×. Any future cap for the remaining
stage-1 pass should assume ~$3/run for nx/rich and ~$4.50/run for
click-class candidates: nx-t7 + nx-t8 + rich-u6 + rich-u7 stage 1
≈ $24 ± 4 — i.e. roughly another full $25 cap — before the A/B's
$18 is even reached, and the A/B gate figure needs revising upward
for any click band member.

## What a follow-on wave needs

1. A fresh screening cap decision (≈$25 at the calibration above)
   to finish stage 1 for nx-t7, nx-t8, rich-u6, rich-u7.
2. Band ≥ 4 total before the pre-registered A/B can run; currently
   1 (click-c2). Even a complete stage-1 pass guarantees nothing —
   six of the seven candidates screened in waves 1 + 4-A passed
   base 2/2.
3. If a click task is in the A/B set, the click orientation fixture
   (`evals/fixtures/click-orientation.md`) must be written and
   committed before any click A/B run (per preregistration).
