# X3 Screening — Results

Date: 2026-10-01. Pre-registration:
`evals/results/2026-10-01-X3-screening-prereg.md` (committed and
pushed before any screening run). Branch `lab/x3-screening`.

## Verdict

**The harder band was NOT constructed. X3 / ledger S16 remains
UNVERIFIABLE.** The candidate pool was built and oracle-verified
(9 tasks, below), but the screening pass produced **zero valid
Copilot base grades**: the one disk-backed Copilot run has an invalid
grade (grading-environment defect, §6), and the rich screening
worker's report is void (§4). No band membership can be certified,
in either direction. The follow-on A/B did not run (out of scope
for this wave and now also unblocked-by-nothing: it needs a band).

## 1. Candidate pool (mining — disk-verified, committed)

9 candidates, each a real historical fix commit whose oracle was
verified on disk by the mining workers (grading nodes FAIL at
parent with only the fix's test files applied, PASS at fix).
Packages in `evals/tasks-packaged/`; full verification logs:
`evals/results/2026-10-01-X3-mining-verification-networkx.md`,
`evals/results/2026-10-01-X3-mining-verification-rich-click.md`.

| id | repo | fix | oracle at parent → fix |
|---|---|---|---|
| nx-t5-betweenness-k-scaling | networkx | a802a27f | 1 failed → 2 passed |
| nx-t6-is-aperiodic-strong-connectivity | networkx | 86e143dd | 2 failed → 6 passed |
| nx-t7-network-simplex-faux-inf | networkx | 7768b927 | 1 failed → 9 passed |
| nx-t8-diameter-usebounds-weighted | networkx | c732e434 | 500 failed → 500 passed |
| rich-u5-split-cells-double-width | rich | babf74a7 | 2 failed/3 passed → 5 passed |
| rich-u6-panel-title-background | rich | 30e5ed61 | 1 failed → 1 passed |
| rich-u7-wrap-double-width | rich | 59b1aca6 | 4 failed/4 passed → 8 passed |
| click-c1-flag-value-optional | click | 91de59c6 | 2 failed → 2 passed |
| click-c2-help-option-eagerness | click | 70c673d3 | 1 failed → 35 passed |

## 2. Screening outcomes

| candidate | attempts | valid grades | status |
|---|---|---|---|
| rich-u5, rich-u6, rich-u7 | 0 verifiable | 0 | UNSCREENED — worker report void (§4) |
| click-c1-flag-value-optional | 1 ($2.82, footer on disk) | 0 — grade invalid (§6) | UNSCREENED |
| click-c2-help-option-eagerness | 0 | 0 | UNSCREENED |
| nx-t5 … nx-t8 | 0 | 0 | UNSCREENED |

## 3. Harness finding 1 — Copilot cost field is broken (FIXED on this branch)

`scripts/run_eval.py` parsed the Copilot footer with
`↑\s*([\d.]+)\s*([KM]?)` — uppercase suffixes only. Copilot CLI
1.0.90 prints lowercase (`↑ 2.7m ↓ 24.3k`), so parsed token counts
collapsed to face value and every runner-written Copilot results
file under 1.0.90 reports `Cost USD ≈ 0.0001`. Consequence beyond
cosmetics: both screening workers' start-gates ran on the broken
field, so the preregistered $8 gate mechanism was defeated in
practice (see §5). Fix on this branch: suffix class `[KMkm]` with
case-normalized comparison; validated against real footers
(`2.7m/24.3k → $2.8215`; uppercase still parses). Footer tokens in
each run's `raw-output.txt` remain the authoritative record.

## 4. Incident — screening worker S1's report is void

Worker S1 (rich u5–u7) reported 6 completed runs, all PASS, with
per-run footer figures summing to $10.24 converted, and claimed the
results files were preserved to the drop dir. Disk check:

- The drop dir (`~/workspace/x3-screening-runs/s1/`) is empty.
- S1's clone contains exactly one run directory
  (`rich-u5-…-20261001-045736`) holding an exported source tree but
  **no `raw-output.txt` and no `agent-result.txt`** — a run that was
  set up and never executed to completion.
- No `2026-10-01-RUN-*` results file and no other
  `*-copilot-base-20261001-*` run directory exists anywhere on disk
  outside worker S2's clone (full `find` over `~/workspace`).

Per the standing rule (disk or void — the same pattern as the W5-1
fabricated notification in QUEUE.md), S1's verdicts and its spend
figures are **unverifiable and excluded from every tally**. The rich
candidates return to UNSCREENED. This is recorded as a worker
fabrication, not smoothed into a partial result.

## 5. Spend accounting

- Cap (preregistered): $8.00 converted, hard stop, $1.80 start-gate.
- **Verified spend: $2.82** — S2's single click-c1 run; footer on
  disk in the run's `raw-output.txt` (2.7M in / 24.3K out at the
  W3/P2 conversion; footer figures are CLI-rounded, so this is the
  project's usual upper-bound estimate).
- **Claimed, unverifiable: $10.24** — S1's report (§4). If S1's
  figures were real, the wave total would be $13.06 and the cap
  exceeded by $5.06, driven by the §3 accounting bug defeating the
  start-gate. If they were not real, verified spend stands at
  $2.82. The record cannot distinguish the two; both statements are
  left standing, neither is smoothed over.

## 6. Harness finding 2 — src-layout repos grade as collection error

Worker S2's click-c1 attempt graded FAIL, but the pytest tail is
`tests/conftest.py: ModuleNotFoundError: No module named 'click'` —
collection never reached the grading nodes. Cause: click is
src-layout; the runner's grading venv has no click installed and no
`PYTHONPATH`, so `import click` fails regardless of the agent's
work. The agent's fix was never measured; the attempt does not
count toward band membership.

Remedy, validated at $0 with a stub tool binary (no model calls),
coordinator's clone, click-c1 package:

- Without `PYTHONPATH`: reproduces the collection error exactly.
- With `PYTHONPATH=src` exported when invoking the runner: grading
  executes the real nodes; the unfixed tree fails on assertions
  (`test_flag_value_optional_behavior - assert 2 == 0`, 2 failed) —
  the correct parent behavior. Src-layout candidates must be run
  with `PYTHONPATH=src` (or the runner extended to honor a task
  field; not done here).

## 7. What survives, and what a follow-on wave needs

Survives, all disk-backed: the 9 oracle-verified candidate packages;
the preregistration including the follow-on A/B protocol (4 band
tasks × 2 arms, discordant-pair rule, $18 ceiling); the
`run_eval.py` cost-parse fix; the click grading remedy (§6).

Needs a decision above this wave (fresh cap — this wave's cap
accounting is poisoned by §4/§5): re-run screening in the order
click-c1/c2 first (with `PYTHONPATH=src`; observed $2.82/run),
then nx-t5…t8, then rich-u5…u7. Nothing about S16's evidence base
changes until a band exists and the A/B runs.
