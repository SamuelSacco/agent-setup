---
session_id: 2026-09-30-1514-helm-roster-drift
tool: claude-code
model: Muse Spark (subagent, parent-directed)
started: 2026-09-30 15:14 EDT
status: complete
intent: Backlog X20 — reconcile roster narrative drift (wiki note vs packet vs canonical/) into one disk-verified roster decision, append-only.
---

# Session: Roster drift (X20)

## Intent
Parent-directed worker run: disk-verify the three roster stories
against `canonical/agents/` and the claims ledger; record one roster
decision in one place with append-only dated corrections; retire —
do not build — packet names with no canonical file. Branch
`fix/roster-drift` off phase-2 head cf65806, own clone
`~/workspace/p3/roster`. No API spend.

## Starting state
- Orientation read: AGENTS.md, wiki/index.md, wiki/data-model.md,
  wiki/log.md tail.
- Three sources disagree: W2 note (7 default agents), packet
  roster v2 (6 default + 2 provisional), canonical/ on disk (12).

## Turn log

### 15:14 — disk verification
- **Intended:** verify every roster name against files, installer
  code, git history, and ledger S14.
- **Tried:** `ls canonical/agents/` + frontmatter `name:` sweep;
  `install_agents()` in `scripts/adapters.py`; full-tree scan of
  `git rev-list --all` for task-runner/evaluator/explorer files;
  grep of `canonical/` + `scripts/`; read W2 note, packet roster
  bullet + corrections, research roster doc
  (`hidden_files/research/2026-09-30-P2-roster-v2.md`), ledger S14.
- **Happened:** 12 canonical files; installer globs and emits all
  12 with no tier filter. task-runner/evaluator/explorer: no file
  at head or in any commit tree. evaluator spec (no edit)
  contradicts data-scientist on disk (edit in tools_hint).
  explorer double-counts code-explorer (one file). Packet
  demotions (backend/ux-ui → skill, tdd-guide/doc-updater dropped)
  never landed. S14 current status PARTIAL (audit-downgraded),
  12/12 agents + 8/8 skills invoked in both tools — the W2 note's
  UNVERIFIED line is overtaken and the triage correction's
  "S14 PROVEN" citation is stale.

### 15:20 — decision + corrections (append-only)
- **Intended:** one roster decision in one place; pointer
  corrections in packet and backlog; no history rewritten, no
  agent files created.
- **Tried:** appended X20 correction section to
  `wiki/notes/v2-roster.md` (the decision); appended dated
  correction to `docs/phase2-packet-2026-09-30.md`; appended X20
  resolution bullet to `docs/experiments-backlog.md`; updated the
  [[v2-roster]] line in `wiki/index.md`.
- **Happened:** decision recorded — roster of record = the 12
  canonical agents as installed; task-runner/evaluator
  not-built/retired; explorer retired as a separate entry.

## Learned
- The installer is the roster: `install_agents()` emits every
  file in `canonical/agents/`; any default/optional/provisional
  language in narrative docs describes a proposal, not the setup,
  until a filter exists in the adapter.
- A correction can itself go stale: the triage correction cited
  S14 as PROVEN after the audit had already downgraded it to
  PARTIAL. Corrections must cite the ledger's current status.

## Outcome
complete — X20 closed. One decision in `wiki/notes/v2-roster.md`
(2026-09-30 X20 correction); packet + backlog carry dated pointer
corrections. No canonical files created or changed. Spend: $0.
