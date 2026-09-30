---
session_id: 2026-09-30-1433-claude-bigmodel-orientation
tool: claude-code
model: opus (CLI alias; envelope model ID recorded in results)
started: 2026-09-30 14:33 EDT
status: complete
intent: Test whether the S12 orientation effect survives a model-tier change (Haiku 4.5 → Opus), same tasks, same protocol, $14 hard cap.
---

# Session: P3 big-model orientation A/B (E1)

## Intent
Samuel directed (2026-09-30 14:24 ET) spending half the topped-up API
budget on experiments with the best models. This stream re-runs the
W3 orientation A/B (NetworkX T1–T4, base vs +orientation) on Opus
under the S12 decision rule.

## Starting state
- Branch `exp/bigmodel-orientation` off `phase-2` @ 3556e46, clone at
  ~/workspace/p3/bigmodel.
- Prior evidence: S12 PROVEN on Haiku (NetworkX 8/8 vs 6/8 combined;
  Rich null). Two published frontier-model nulls motivated the test.
- Fixtures verified: orientation artifact sha256
  ea8015523f0ec0142b891d27421b63dfbf70b1f275352bc58d87b2ef503d9515
  (byte-identical to W3 assets); prompts verbatim W3 assets;
  NetworkX mining clone clean; Claude Code 2.1.285.

## Turn log

### 14:33 — setup + preregistration
- **Intended:** clone, orient, package T1/T3/T4 (T2 package exists),
  preregister before any run.
- **Tried:** git clone + branch; read repo AGENTS.md, run_eval.py,
  W3 prereg/results, second-codebase runner; copied fixtures
  read-only from mining dirs with hash verification.
- **Happened:** packages + prereg written
  (evals/results/2026-09-30-P3-bigmodel-prereg.md); $14 hard cap,
  projection/cut/fallback rules fixed in the prereg. Committed and
  pushed before the first run launches.

### 14:47 — calibration + NetworkX set
- **Intended:** run T1 base as calibration, then complete pairs in
  prereg order.
- **Tried:** run-eval.sh, --model opus, packaged tasks, W3 source
  clone + venv.
- **Happened:** envelope confirms canonical model `claude-opus-5-5`.
  Run 1 cost $0.189683 (heavy prompt-cache reads) — fallback rule
  never triggered, nothing cut. NetworkX: base 3/4, +orientation
  3/4, zero discordant pairs. T1 base PASSES on Opus (Haiku failed
  it); T4 FAILS on both arms — neither agent changed library code;
  both reported the symptom unreproducible against their own density
  probes. Set spend $1.464014.

### 15:40 — Rich set (prereg trigger fired; addendum e706f37 first)
- **Intended:** U1–U4 pairs on Opus under the same rule.
- **Happened:** base 3/4, +orientation 3/4, zero discordant pairs.
  U3 fails identically in both arms (`test_zwj`, `assert 1 == 2`) —
  same signature as Haiku. Set spend $1.582532.

### 15:55 — write-up
- **Intended:** results file, ledger, wiki, verdicts per prereg.
- **Happened:** evals/results/2026-09-30-P3-bigmodel-ab.md written.
  Ledger: new claim S18 (UNVERIFIABLE at opus tier) + scope note on
  S12 — separate claim chosen because S12's PROVEN was earned under
  its own pre-registration at the Haiku tier; rewriting its status
  would falsify the record. Wiki note orientation-real-code updated;
  index + log appended. Mining clones verified clean after all runs
  (no escapes). Harness caveat found: run-eval.sh result filenames
  are date-granular — the Opus T2 base run overwrote the S17 proof
  RUN file in the working tree (original preserved in git history);
  recorded in the results file.

## Learned
- The orientation effect, as measured, is tier-dependent: it bought
  solves exactly where the Haiku base left headroom (T1). On
  claude-opus-5-5 base solves T1 unaided; remaining failures are
  concordant. Orientation still charges ~+9% cost per run.
- Opus per-task envelope cost can be LOWER than Haiku on the same
  tasks (fewer turns, cache-dominated tokens): NX set $1.464 vs
  Haiku $2.132. Per-token price is the wrong unit for budgeting
  agent tasks; measure per-task.
- Failure mode at the top tier: on T4 both agents empirically
  "refuted" the symptom report and changed nothing, while the
  oracle tests still discriminate. Self-verification against the
  prompt's example parameters is not the grading oracle.

## Outcome
complete — 16/16 runs executed and disk-graded; verdict UNVERIFIABLE
at the opus tier on both codebases (S18); total spend $3.046546 of
the $14.00 cap.
