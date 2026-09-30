---
session_id: 2026-09-30-1119-helm-copilot-orientation-ab
tool: helm (subagent)
model: Muse Spark (coordinator); eval runs use Copilot CLI 1.0.89 BYOK claude-haiku-4-5-20251001
started: 2026-09-30 11:19 EDT
status: partial
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

### 11:21 — prereg committed before any run
- **Intended:** lock protocol before running.
- **Tried:** wrote evals/results/2026-09-30-P2-copilot-ab-prereg.md (8 tasks, 2 arms, W3 base reused for T1/T3, Claim C rule mirroring Claim B, $4 cap, run order, stop rules); committed b4bde7d, pushed.
- **Happened:** prereg on origin/phase-2 before first run.

### 11:24 — T1 +orient (smoke run of the new runner)
- **Intended:** validate harness end-to-end on the first scheduled run.
- **Tried:** runner.py (~/workspace/p2/copilot-ab/) — git-archive isolation, root CLAUDE.md = frozen orientation text, disk grading, footer token parse, mining-clone cleanliness assert.
- **Happened:** PASS — 3/3 grading tests, own-tree diff 4 insertions/1 deletion in 1 file, no mining-clone dirt. Wall 483s (W3 base: 198s). Converted cost $2.19 (2.0M in / 38.7k out) — Copilot's token volume on the orientation arm is ~40% above its T1 base run; budget gate will bind early. Remaining sequence launched in prereg order with the $3.40 start-gate enforced per run.

### 11:33–11:45 — remaining runs; budget gate binds
- **Intended:** complete the matrix in prereg order.
- **Tried:** T3 +orient, R2 base, then R2 +orient / R1 / R3 / T2 pairs under the runner's budget gate; R4/T4 last per prereg.
- **Happened:** T3 +orient PASS (4/4, $0.63, 130s). R2 base PASS (2/2, $1.80, 211s) — cumulative $4.63 crossed the gate; all further runs skipped by the gate and R4/T4 never started. Verdict over 2 completed pairs (T1, T3 concordant passes): Claim C UNVERIFIABLE. Results written to evals/results/2026-09-30-P2-copilot-ab.md; ledger S16 added; [[orientation-real-code]] note updated.

## Learned

- Copilot CLI's token volume is the binding constraint for eval design:
  1.7–2.0M input tokens on ISMAGS-scale tasks (nearly all cached, but
  counted at full rate under the W3 conversion) — 3–9× Claude's
  converted cost per identical task. A 16-run Copilot matrix at this
  burn rate prices at ~$15–25 converted, not $4.
- Copilot base has passed every real-code task it has run in this
  project (T1, T3, R2). Both Claude discordant pairs are tasks
  Copilot base solves unaided, so orientation headroom in Copilot must
  be sought on tasks Copilot base fails — none observed yet.
- The VM clock is UTC; any local-time gate in eval tooling must pin
  America/New_York explicitly.

## Outcome
partial — Claim C (S16) UNVERIFIABLE: 2 of 8 pairs completed, both
concordant passes; 11 planned runs stopped by the preregistered budget
gate; total new spend $4.63 converted vs ~$4 cap (one run's overshoot,
recorded in the results file). Results, ledger S16, and the
[[orientation-real-code]] note update are committed with this session.
Open: a Copilot orientation test with headroom needs tasks Copilot
base fails, or a budget sized to Copilot's token volume.