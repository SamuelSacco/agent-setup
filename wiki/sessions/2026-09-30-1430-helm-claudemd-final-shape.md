---
session_id: 2026-09-30-1430-helm-claudemd-final-shape
tool: helm (subagent)
model: Muse Spark (coordinator); probes use Claude Code 2.1.285 / Copilot CLI 1.0.89, model claude-haiku-4-5-20251001
started: 2026-09-30 14:30 EDT
status: complete
intent: Prove the no-CLAUDE.md final shape (native AGENTS.md load + guard) and execute the drop on branch change/no-claudemd, or refute it.
---

# Session: CLAUDE.md final-shape proof (W3)

## Intent
Samuel's preference is a tool-agnostic setup with no CLAUDE.md if nothing
Claude-specific requires one. Task W3: delete CLAUDE.md on
`change/no-claudemd`, ship a guard that fails on the version floor, a
bridgeless CLAUDE.md, or a failed live marker probe; prove the final shape
live in both tools; negative-control the guard; amend ledger claim C4.
The proof gates the deletion — if the drop test fails, restore and report
REFUTED.

## Starting state
- Branch `phase-2` @ 3556e46 cloned to ~/workspace/p3/claudemd; working
  branch `change/no-claudemd` created from it.
- Prior evidence: W5 canary probes (evals/results/2026-09-30-P2-claudemd-drop.md)
  — native load 2/2, suppression trap 2/2, verdict PARTIAL with a
  keep-the-bridge recommendation. This session re-tests under Samuel's
  14:24 ET directive (execute with proof, guard replaces the bridge).
- CLAUDE.md at start: `@AGENTS.md` + annex (a) verify loading with
  `/context`; (b) pointer to docs/tips-claude.md for /advisor, output
  styles, .claude/rules/. AGENTS.md already routes tool-specifics to
  docs/tips-claude.md; annex item (a) changes referent after the drop
  (check AGENTS.md, not CLAUDE.md, in /context).
- Toolchain: claude 2.1.285, copilot 1.0.89 (~/workspace/tools/bin/).

## Turn log

### 14:30 — Orientation + recon
- **Intended:** Ground the work in repo conventions before editing.
- **Tried:** Read AGENTS.md, CLAUDE.md, claims ledger (claim C4 covers
  AGENTS.md/CLAUDE.md discovery), W5 results, run-eval.sh/run_eval.py
  (binary paths, apiKeyHelper pattern, Copilot BYOK env pattern),
  wiki/index.md, wiki/log.md tail, session template.
- **Happened:** Recon complete. Ledger claim to amend: C4. Wiring point:
  run_eval.py main() has no preflight; guard static mode fits as one.

## Turn log

### 14:30 — Orientation + recon
- **Intended:** Ground the work in repo conventions before editing.
- **Tried:** Read AGENTS.md, CLAUDE.md, claims ledger (claim C4 covers
  AGENTS.md/CLAUDE.md discovery), W5 results, run-eval.sh/run_eval.py
  (binary paths, apiKeyHelper pattern, Copilot BYOK env pattern),
  wiki/index.md, wiki/log.md tail, session template.
- **Happened:** Recon complete. Ledger claim to amend: C4. Wiring point:
  run_eval.py main() has no preflight; guard static mode fits as one.

### 14:35 — Delete + guard
- **Intended:** Remove CLAUDE.md on the branch; ship the guard.
- **Tried:** `git rm CLAUDE.md`; wrote `scripts/check-agents-md-load.sh`
  (checks a/b/c per header); wired it into run_eval.py main() as a
  `--static` preflight with `--skip-preflight` bypass.
- **Happened:** Static guard on the branch tree: PASS (a) 2.1.285 ≥
  2.1.277, PASS (b) no CLAUDE.md. Preflight failure path proven against
  a stub tree (run-eval exit 2 before spend).

### 14:40 — Live proof, final shape
- **Intended:** Prove AGENTS.md loads with no CLAUDE.md, both tools.
- **Tried:** Guard `--runs 2`; two manual Claude evidence probes in
  /tmp/w3proof/final; one Copilot BYOK probe, same project/prompt.
- **Happened:** Claude 2/2 marker (debug log: "no CLAUDE.md found;
  AGENTS.md loaded"), costs $0.0120/$0.0139. Copilot 1/1 marker,
  15.8k in / 179 out.

### 14:50 — Negative controls
- **Intended:** The guard must catch the suppression trap, not just
  pass the happy path.
- **Tried:** Stub tree (annex-only CLAUDE.md): guard default mode;
  guard `--skip-static` live-only; bridged tree static check.
- **Happened:** Default: exit 1 at (b). Live-only: exit 1 at (c),
  probe answered NOT LOADED — suppression reproduced live. Bridged
  tree: exit 0.

### 15:00 — Wiring run + docs
- **Intended:** Prove the eval loop still grades end-to-end with the
  preflight wired in; amend the record.
- **Tried:** Packaged nx-t2 eval via run-eval.sh (preflight active).
  Amended ledger C4, packet Finding 4 (dated correction note), README
  tree, docs/tips-claude.md, docs/feedback-loop.md, wiki note
  [[instruction-files]].
- **Happened:** Wiring run PASS (1/1 nodes, 9 turns, $0.108047, 248 s)
  with guard PASS lines first. Harness friction, logged honestly: the
  exec layer backgrounded two earlier launches of the same test, which
  kept running concurrently and completed their tool stages ($0.245 +
  $0.161) — duplicates disclosed in the results cost log. The runner
  overwrote the S17 RUN results file by design (same dated name);
  S17's version was restored from phase-2 before commit.

## Learned
- The `@AGENTS.md` bridge can be replaced by a guard: the three
  invariants (version floor, no bridgeless CLAUDE.md, live marker
  probe) cover every failure mode W5 found, and the live probe alone
  catches suppression (NOT LOADED) even if the static check is bypassed.
- Annex-loss accounting for the drop: /context tip now refers to
  AGENTS.md; InstructionsLoaded no longer fires for the main file.
  Both accepted in ledger C4's amendment.
- Backgrounded exec sessions may keep child processes running after a
  "completed" notification; verify process state on disk, not from the
  notification.

## Outcome
complete — CLAUDE.md deleted on `change/no-claudemd`, guard shipped and
wired, final shape PROVEN (Claude 2/2, Copilot 1/1), negative controls
exit 1, ledger C4 amended. Evidence:
`evals/results/2026-09-30-P2-claudemd-final-shape.md`. Total spend
≈ $0.59 (incl. two disclosed duplicate wiring attempts).
