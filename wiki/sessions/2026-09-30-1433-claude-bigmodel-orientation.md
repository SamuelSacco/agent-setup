---
session_id: 2026-09-30-1433-claude-bigmodel-orientation
tool: claude-code
model: opus (CLI alias; envelope model ID recorded in results)
started: 2026-09-30 14:33 EDT
status: in-progress
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

## Learned
- (pending runs)

## Outcome
in-progress
