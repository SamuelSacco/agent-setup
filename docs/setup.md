# Setup — follow along

Goal: from zero to both agents working off one root in ~15 minutes.

## 1. Install the tools

```bash
# Claude Code (see https://code.claude.com for the current installer)
claude --version

# GitHub Copilot CLI
copilot --version
```

## 2. Authenticate (one human step each — do not share credentials)

```bash
claude auth login     # follow the browser/device flow
copilot login         # GitHub device flow (gh auth alone is NOT sufficient)
```

Verify:
```bash
claude auth status    # loggedIn: true
```

## 3. Get this workspace

```bash
git clone <this-repo> agent-setup
cd agent-setup            # <- always launch agents from here
```

## 4. Install capabilities into both tools

```bash
./scripts/install.sh
```

This reads `canonical/` and writes each tool's native layout. Add a skill 
later = one new file in `canonical/skills/` + re-run this script.

## 5. First session

```bash
claude       # or: copilot
```

Ask: "Orient per AGENTS.md, then tell me what this workspace is."

Expected: the agent reads `wiki/index.md`, creates a session file under 
`wiki/sessions/`, and can explain the layout. If it doesn't, the root 
instructions didn't load — check you launched from the repo root.

## 6. Prove it (don't trust it)

Run the evals in order as auth allows: E1 (install parity) → E4 (failure 
capture) → E2 (cross-tool continuity). Record verdicts in 
`docs/claims-ledger.md`. Status (2026-09-30): E1/E2 outcomes are recorded in the ledger as S1/S2 — PROVEN at scoped wording (see their audit notes); the ledger, not this checklist, is the live definition of "done."

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| Skill not listed in one tool | Launched outside repo root, or adapter format drift — re-run install, then check the tool's skill path |
| Instructions ignored | Wrong root: `AGENTS.md`/`CLAUDE.md` load from the launch directory upward |
| MCP server missing in one tool | `.mcp.json` (Claude) vs `.github/mcp.json` (Copilot) — re-run install; check server name match |
| Sessions not shared | Agent didn't follow the lifecycle — check `wiki/sessions/` for the file; reinforce via AGENTS.md §2 |
