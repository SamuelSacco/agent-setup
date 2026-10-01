---
session_id: 2026-10-01-0537-helm-x16-install-surface
tool: claude-code
model: Muse Spark (subagent, Wave 4-B)
started: 2026-10-01 01:37 EDT
status: complete
intent: Run the two X16 install-surface probes (Claude remote marketplace, skills --copy) in scratch-HOME isolation and record verdicts.
---

# Session: X16 install-surface probes

## Intent
Close the two UNVERIFIABLE cells left by the P2 install matrix: remote
(GitHub) Claude marketplace add/install, and `npx skills --copy` mode.
One probe each, matrix protocol, scratch HOME only.

## Starting state
- Branch `lab/x16-install-surface` off origin/master 048e5ff.
- Local marketplace path PROVEN; `--copy` DOCS-ONLY (install-scopes §1a/§1b).
- Prereg committed before any probe run:
  `evals/results/2026-10-01-X16-install-surface-prereg.md`.

## Turn log

### 01:37 — Orientation + prereg
- **Intended:** read install matrix docs, fix commands/criteria before running.
- **Tried:** read `docs/install-scopes-2026-09-30.md`, cheatsheet §5,
  P2 matrix, backlog X16; wrote prereg.
- **Happened:** commands taken unchanged from cheatsheet §5 (probe 1)
  and install-scopes §1a source/skill (probe 2, `--copy` added).

## Learned
<filled at hardening>

## Outcome
<filled at hardening>

### 01:38–01:47 — Probes (appended at hardening)
- Probe 1 (remote marketplace): add exit 0 via anonymous HTTPS clone;
  install exit 0 scope user; payload at scratch
  `.claude/plugins/cache/claude-plugins-official/commit-commands/ab024cdcfa7c/`;
  `plugin list --json` enabled true; details inventory returned. PROVEN.
- Probe 2 (`skills --copy`): add exit 0; zero symlinks in canonical or
  Claude target; `diff -r` vs fresh source clone empty on all pairs;
  no `~/.copilot/skills` created (canonical store is Copilot's dir);
  source-internal symlink dereferenced with identical content. PROVEN.
- Results: `evals/results/2026-10-01-X16-install-surface.md`; backlog
  X16 closed; ledger S27 added; install-scopes §1a amended.
- Learned: (1) remote marketplace needs no auth for public repos —
  Claude falls back to HTTPS when SSH is unconfigured. (2) `--copy`
  exit code is 0 where symlink mode's was 2. (3) `--copy` dereferences
  symlinks internal to a skill.
- Outcome: complete. Spend $0.00.
