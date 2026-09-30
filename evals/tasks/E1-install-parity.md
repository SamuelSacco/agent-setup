# E1 — One-install parity

**Claim S1:** A skill defined once in `canonical/` is discoverable by both 
Claude Code and GitHub Copilot CLI after `./scripts/install.sh`.

**Pre-registered threshold:** PASS if both tools list `session-harden` as an 
available skill in a fresh session launched from the repo root. FAIL otherwise.

## Steps
1. `./scripts/install.sh`
2. Claude Code (from root): list available skills; record whether 
   `session-harden` and `wiki-lint` appear.
3. Copilot CLI (from root): list available skills; record the same.
4. Invoke `session-harden` by name in each tool on an empty session; PASS 
   requires the tool to load the skill body, not just the name.

## Status
- File placement: PROVEN locally (adapters write both layouts).
- Live discovery + invocation: **PROVEN both tools** (2026-09-30) — Copilot:
  `results/2026-09-30-E1-partial.md`; Claude:
  `results/2026-09-30-E1-claude.md`. **E1 verdict: PASS.**
- Constraint found: headless Claude runs block on file-write permission
  prompts; eval runs need an explicit permission mode.
