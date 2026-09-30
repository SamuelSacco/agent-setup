---
session_id: 2026-09-30-0745-claude-code-phase2-coordination
tool: claude-code
model: coordinator (children: claude-haiku-4-5-20251001 for eval runs)
started: 2026-09-30 07:45 ET
status: in-progress
intent: Phase 2 — install-surface matrix, CLAUDE.md-drop test, ECC mining, real-codebase A/B; evidence over Samuel's intuitions, on branch phase-2 only.
---

# Session: Phase 2 coordination

## Intent
Samuel (07:41 ET): V1 frozen; ramp up. Be more aggressive and curious, token-max, run the setup against real codebases, derive the agent/skill roster from evidence (incl. ECC), and settle his open questions: what each install path actually does per tool, and whether CLAUDE.md is still needed. He reviews V1 in ~16 min; the 14:00 dry run needs W3 initial results by 13:30.

## Starting state
- V1 frozen: tag `v1` = commit 2021d60 (verified `git rev-parse v1^{commit}`).
- Branch `phase-2` created from master and pushed. Master and tag untouched from here.
- Anthropic API balance ~$18.23 (Samuel-reported). Phase 2 hard cap: **$15 total**, every run logged. Allocations: W1 $3.00, W5 $1.00, W2 $0.75, W3 $9.00, reserve $1.25.
- CLIs: claude 2.1.285, copilot 1.0.89 (`~/workspace/tools/bin/`).
- Auth pattern (from V1 evidence): scratch `.claude/settings.json` with `apiKeyHelper` → helper script; Copilot BYOK env vars, key via helper stdout, never printed.
- Unattended allow-all authorization (Samuel 2026-09-30 01:44) covers scratch/eval dirs only. `--dangerously-skip-permissions` is refused under root — use `--permission-mode acceptEdits` + `--allowedTools`.

## Turn log

### 07:45 — Phase 2 fan-out
- **Intended:** Spawn one subagent per workstream in parallel; each works in its own clone under `~/workspace/p2/<ws>/` on branch phase-2, commits locally, coordinator integrates into the main phase-2 branch.
- **Tried:** W1 install matrix, W5 CLAUDE.md-drop, W2 ECC mining, W3 real-codebase A/B (pre-registration required before any run).
- **Happened:** pending — results appended as they land.

### 07:47 — W2 ECC mining landed (first return)
- **Intended:** ECC inventory, license check, ports, derived roster.
- **Tried:** Child mined affaan-m/ECC at c70874f (v2.2.2); LICENSE read in full: MIT. 668 items inventoried individually.
- **Happened:** 19 ported into canonical/ (9 agents, 6 skills, 4 MCP), 223 PORT-WITH-CHANGES, 426 SKIP; commands/hooks/rules skipped as classes with reasons. Spend $0.00. Integrated into phase-2 as bd1900c and pushed. V1 data-scientist and ux-ui both demoted to optional in the derived roster — Samuel's suspicion about the V1 roster confirmed by inventory.

### 07:48 — W5 CLAUDE.md-drop landed
- **Intended:** Settle whether CLAUDE.md can be dropped on Claude 2.1.285 (four canary arms).
- **Tried:** Arms A (control, bridge), B (no CLAUDE.md), C (annex-only CLAUDE.md, no import), D (both-files via user settings), 2 clean runs each.
- **Happened:** Verdict PARTIAL. Native AGENTS.md load PROVEN when no CLAUDE.md exists in cwd/ancestors (B, 2/2). Trap PROVEN (C, 2/2): annex-only CLAUDE.md silently suppresses the shared file — the bridge is load-bearing. Arm D: both-files mode IS settable headlessly via user settings `pluginConfigs` (`instructionFiles: claude-md-and-agents-md`), 2/2 both canaries. Recommendation: keep the `@AGENTS.md` bridge; dropping loses the annex + InstructionsLoaded hook firing and adds a silent ancestor-suppression failure mode (bit the child's first runs — repo's own ancestor CLAUDE.md contaminated in-repo scratch; clean runs moved to /tmp, deviation documented). Spend $0.1204 of $1.00 cap. Integrated as c8f14ed (author rewritten to Helm identity — child's commit carried Samuel's private email and GitHub rejected the push, GH007).
- **Phase 2 spend so far: $0.1204 / $15.**

## Learned
<filled at hardening>

## Outcome
in-progress
