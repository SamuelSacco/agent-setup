---
session_id: 2026-09-30-1119-helm-copilot-orientation-ab
tool: helm (subagent)
model: Muse Spark (coordinator); eval runs use Copilot CLI 1.0.89 BYOK claude-haiku-4-5-20251001
started: 2026-09-30 11:19 EDT
status: in-progress
intent: Measure the orientation effect in Copilot CLI (base vs +orientation) on the same 8 NetworkX tasks used for the Claude A/B — the missing half of the "one setup, two agents" headline.
---

# Session: Copilot orientation A/B

## Intent
Phase 2 measured orientation on Claude (combined 8/8 vs 6/8). Copilot only
has base results on T1/T3 from W3. Run Copilot base vs Copilot +orientation
on the same 8 tasks, same prereg discipline, disk grading only.

## Starting state
- Branch phase-2 @ 4489b04, clean.
- All 8 task fixtures survive: T1–T4 in ~/workspace/p2/w3/scratch/
  (runner.py TASKS + assets/prompt-T*.txt), R1–R4 in
  ~/workspace/p2/portverify/repl/ (repl_runner.py TASKS + assets).
- Orientation artifact: assets/orientation.md byte-identical in both
  scratch dirs (diff verified). Placed as root CLAUDE.md in the +orient
  arm, exactly as the Claude arm did; Copilot CLI reads root CLAUDE.md
  natively (docs/tips-copilot.md, PROVEN research).
- Mining clone ~/workspace/p2/w3/scratch/.infra/nx-src clean @ 92f497e2e.
- W3 Copilot base results exist for T1 (pass, ~$1.49) and T3 (pass,
  ~$0.47), same protocol/model/prompts — reused per prereg.

## Turn log

### 11:19 — orientation
- **Intended:** locate fixtures, prereg, orientation artifact, Copilot invocation pattern.
- **Tried:** read realcode prereg + results; read w3 runner.py and repl_runner.py; diff orientation assets; check Copilot binary + footer format.
- **Happened:** all fixtures intact; Copilot at ~/workspace/tools/bin/copilot (1.0.89), BYOK env per w3 runner; cost conversion from footer tokens at $1/M in, $5/M out (upper bound).

## Learned

## Outcome
