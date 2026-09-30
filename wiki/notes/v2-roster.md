---
id: v2-roster
title: Decision — V2 default roster derived from ECC inventory (P2 W2)
type: decision
status: active
created: 2026-09-30
updated: 2026-09-30
verified: 2026-09-30
relates_to: [install-surfaces, session-lifecycle]
sources: []
tags: [roster, ecc, canonical]
---

Derived 2026-09-30 (P2 W2, `hidden_files/research/2026-09-30-P2-ecc-mining.md`):
ECC (affaan-m/ECC, MIT) inventoried at 668 items → 19 ported, 223
port-with-changes, 426 skipped. ECC is a catalog, not a setup; the default
roster is selected by job frequency under context rent (ceiling: 7 agents /
8 skills / 4 MCP / 1 hook).

- Default agents: planner, code-reviewer, security-reviewer, tdd-guide,
  build-error-resolver, code-explorer (ECC ports) + V1 backend (kept).
- Default skills: tdd-workflow, verification-loop, search-first,
  codebase-onboarding, documentation-lookup, architecture-decision-records
  (ECC ports) + V1 session-harden, wiki-lint (kept).
- Default MCP: context7, github, sequential-thinking + V1 filesystem-wiki.
  Hook: V1 failure-capture only.
- Demoted to optional: V1 data-scientist (measurement is episodic), V1 ux-ui
  (frontend specialty). Language/stack-specific reviewers, resolvers, and
  pattern skills ship as per-stack optional packs, never defaults.
- Live-tool discovery of the 19 ports is UNVERIFIED (install.sh emits them
  cleanly for both tools; no invocation probe run yet).

## Correction — 2026-09-30 (W2 triage lab)

This note records the earlier W2 derivation and is no longer the roster
of record. The packet (`docs/phase2-packet-2026-09-30.md`) carries a
different roster v2 (default: explorer, code-reviewer, task-runner,
build-error-resolver, security-reviewer, evaluator; provisional: planner,
code-explorer) — which itself exists only on paper: `canonical/agents/`
has no `task-runner` or `evaluator` file, and "explorer" vs provisional
"code-explorer" appear to name the same file. The line above claiming
live-tool discovery is UNVERIFIED is overtaken: ledger S14 (PROVEN,
2026-09-30) live-invoked all 12 agents and 8 skills in both tools.
Three sources currently tell three roster stories; reconciling them is
backlog X20 in `docs/experiments-backlog.md`. Do not cite this note for
the current roster.

## Correction — 2026-09-30 (X20 roster-drift run) — roster of record

This section is the one roster decision. It supersedes the W2
derivation above, the triage correction above, and the packet's
roster v2 as descriptions of the shipped setup. Method: disk only —
`ls canonical/agents/`, frontmatter `name:` fields, `scripts/
adapters.py` `install_agents()`, full-tree scan of every commit in
`git rev-list --all`, and `docs/claims-ledger.md`. No API spend.

Disk-verified verdicts:

- Canonical roster = 12 files — **PROVEN** (on disk at phase-2 head
  cf65806): backend, build-error-resolver, code-architect,
  code-explorer, code-reviewer, data-scientist, doc-updater, planner,
  refactor-cleaner, security-reviewer, tdd-guide, ux-ui.
  `install_agents()` globs `canonical/agents/*.md` and emits every
  file to both tools; no default/optional/provisional filter exists
  in the installer. The shipped roster has no tiers.
- W2 default 7 — **PROVEN** as a subset: all 7 names map to files.
  The other 5 disk files are exactly W2's optional/demoted set
  (code-architect, refactor-cleaner, doc-updater optional;
  data-scientist, ux-ui demoted to optional). W2's split is a
  derivation, not an installed state — the installer installs all 12.
- Packet roster v2 (6 default + 2 provisional) as a shipped roster —
  **REFUTED**. Of its 8 names, 5 map to files (code-reviewer,
  build-error-resolver, security-reviewer, planner, code-explorer);
  3 do not (below). Its demotions never landed: backend, ux-ui,
  tdd-guide, and doc-updater are still canonical agents, and no
  backend or ux-ui skill exists in `canonical/skills/` (8 files,
  unchanged). Source is a proposal with per-entry kill tests
  (`hidden_files/research/2026-09-30-P2-roster-v2.md` §4); backlog X7
  records the planner/code-explorer kill tests as UNVERIFIABLE /
  not run, and no result in the repo tests the other entries.
- `task-runner` — **not built; retired as a roster entry.** No
  `canonical/agents/task-runner.md` at head, in any commit tree, or
  in `canonical/`/`scripts/`. Exists only as a proposal name in the
  research doc, the packet, and the backlog.
- `evaluator` — **not built; retired as a roster entry.** No
  `canonical/agents/evaluator.md` in any commit tree. The research
  spec (data-scientist reborn, read+shell, no edit) contradicts the
  file on disk: `data-scientist.md` keeps its own name and carries
  `tools_hint: [read, edit, shell, search]`. The reborn form was
  never built; data-scientist stays as-is.
- `explorer` as a separate agent from `code-explorer` —
  **REFUTED**. No `explorer.md` in any commit tree; the only
  matching file is `code-explorer.md`. The packet lists both names,
  counting one file twice. `explorer` is retired as a separate
  entry; code-explorer is counted once, in the 12.
- The UNVERIFIED live-discovery line in the W2 derivation above —
  **REFUTED / overtaken**, with a precision fix to the triage
  correction above: it cited ledger S14 as PROVEN. S14's current
  ledger status is **PARTIAL** (audit-downgraded 2026-09-30):
  12/12 agents and 8/8 skills invoked in both tools, 18/19 ports
  invocable as shipped, playwright REFUTED as-shipped in this
  sandbox only. Cite S14 as PARTIAL, not PROVEN.

Decision: the roster of record is the 12 canonical agents above,
as installed by `scripts/install.sh`. Cite this section for the
current roster. No agent files were created in this run: the two
missing names are recorded not-built/retired, not invented.
Backlog X20 closed by this correction. Spend: $0.
