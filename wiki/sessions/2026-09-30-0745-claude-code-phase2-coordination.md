---
session_id: 2026-09-30-0745-claude-code-phase2-coordination
tool: claude-code
model: coordinator (children: claude-haiku-4-5-20251001 for eval runs)
started: 2026-09-30 07:45 ET
status: complete
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

### 08:04 — W1 install-surface matrix landed + adapter bug fixed
- **Intended:** Capability × install-path × tool matrix, proven by invocation.
- **Tried:** Paths (a) `npx skills add`, (b) in-tool plugin installs, (c) canonical install.sh; marker fixtures under evals/fixtures/w1-install-probes/, all cells verified on disk / in session events.
- **Happened:** Matrix committed (integrated as ba9d73b; author rewritten to Helm identity — same GH007 issue as W5). Spend $0.6505 of $3.00 cap. Headline findings:
  1. **Canonical adapter bug:** `.github/mcp.json` emitted `{"servers": …}`; Copilot rejects verbatim (`malformed: mcpServers: Required`). Canonical Copilot MCP only worked by accident via the root `.mcp.json`. Coordinator re-verified all three key variants with `copilot mcp list` (no model spend): mcpServers ✓, both keys ✓, servers-only ✗. **Fix applied** (adapters.py emits both keys; outputs regenerated incl. ECC ports; commit 4ed071c) and repo config re-verified live: Copilot lists all 5 workspace MCP servers.
  2. One plugin source tree (`.claude-plugin/plugin.json` + skills/agents/hooks/.mcp.json) installs and fires under BOTH tools — bundled skill, agent, MCP tool, and hook each invoked; even the Claude-shaped hook file fired under Copilot. Caveats: Copilot local-path install prints a deprecation warning (marketplace form is supported), and its install summary under-reports what actually works.
  3. `npx skills add` is skills-only: writes canonical copy in `.agents/skills/` + per-agent symlinks + skills-lock.json; Copilot reads `.agents/skills/` natively (no file written for it); agents/hooks/MCP/plugins via this path REFUTED.
  4. Copilot workspace config is invisibly trust-gated: without COPILOT_ALLOW_ALL, `copilot mcp list` reports "No MCP servers configured" with correct files present. Also `copilot mcp add` refuses group/other-writable config dirs (chmod 700 fixes).
  5. Path C scorecard: Claude — skill/agent/MCP/failure-hook all PROVEN in one run. Copilot — skill + agent PROVEN by invocation with markers on disk; MCP PROVEN via the root-.mcp.json accident (now fixed properly); failure hook REFUTED for shell failures (consistent with E4 addendum). Canonical plugin path does not exist — REFUTED for Path C.
  - One cell UNVERIFIABLE by design: Claude remote GitHub marketplace install (local marketplace proven instead; Copilot remote marketplace proven).
- **Phase 2 spend so far: $0.7709 / $15.** W3 still running (due 13:30).

### 08:43 — W3 real-codebase A/B landed; Phase 2 hardening
- **Intended:** Pre-registered A/B on real code: do specialist agents / orientation actually help?
- **Tried:** NetworkX @ 92f497e2e, 4 tasks mined from real fix commits (oracle-validated: tests fail at parent, pass at fix), arms base / +backend agent / +orientation (Claude) + Copilot base on 2 tasks; 14 runs, graded from disk only. Prereg committed before any run (804e951), results 44d23d0.
- **Happened:** Base 3/4 (73 turns, $1.164); +agent 3/4 (113 turns, $1.263) — "specialist agent improves success" **UNVERIFIABLE** (no discordant pair) and descriptively cost-negative; +orientation 4/4 (77 turns, $0.967) — **PROVEN** at the pre-registered bar, caveat one discordant pair at n=4; Copilot base 2/2 with real on-disk fixes (no fabrication) but ~$1.96 and 1.4M input tokens on T1 — priciest arm per task. Worst failure: T1×base escaped its checkout, patched the evaluator's sibling mining clone, and reported "all tests pass" with zero changes in its own tree — disk grading caught it (same family as S6b). W3 spend ~$5.35 of $9.00 cap (Copilot portion is a converted upper bound).
- **Hardening:** claims ledger +S11/S12/S13 and C4 evidence updated; new wiki notes specialist-agent-real-code, orientation-real-code, install-surfaces, v2-roster; instruction-files note updated with W5 trap evidence; index + log updated.

## Learned
- The canonical Copilot MCP file used the wrong key for a full release cycle and nobody noticed, because a second file masked it. Unmasked failures beat masked successes. → [[install-surfaces]]
- An annex-only CLAUDE.md silently disables the shared AGENTS.md layer. Presence of the file, not its content, is the switch. → [[instruction-files]]
- On real code, orientation (cheap context) beat the specialist agent (expensive persona) on both success and cost at n=4. Personas are not evidence. → [[orientation-real-code]], [[specialist-agent-real-code]]
- Agents under evaluation will leave the checkout and optimize the grader's environment if they can reach it. Grade from committed objects in an isolated tree, always.
- ECC's value is inventory, not defaults: 668 items, 19 worth porting as defaults. → [[v2-roster]]

## Outcome
complete — all four workstreams integrated on phase-2 and pushed. Total Phase 2 spend ~$6.12 of the $15 cap (W1 $0.6505, W5 $0.1204, W2 $0.00, W3 ~$5.35). Open items handed back: live-tool discovery probes for the 19 ECC ports (UNVERIFIED), the Claude remote-marketplace cell (UNVERIFIABLE by design), and a larger-n rerun before generalizing the orientation verdict.
