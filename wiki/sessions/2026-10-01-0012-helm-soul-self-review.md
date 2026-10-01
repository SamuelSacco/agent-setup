---
session_id: 2026-10-01-0012-helm-soul-self-review
tool: helm-subagent
model: coordinator (W2)
started: 2026-10-01 00:12 EDT
status: complete
intent: Ship the SOUL.md self-evaluation pattern — canonical persona templates, AGENTS.md self-update permission, self-review skill, load + behavioral probes.
---

# Session: SOUL self-review pattern (W2)

## Intent
Samuel's 2026-10-01 00:08 catch: the shipped setup has no instructions allowing or
encouraging the agent to self-evaluate and update its own soul/persona files (the
OpenClaw pattern he runs with Helm). Build it on branch `feat/soul-self-review`.

## Starting state
- master at ce0edbe (public). Worktree ~/workspace/w2-soul.
- ECC mining (hidden_files/research/2026-09-30-P2-ecc-mining.md:137):
  `agent-self-evaluation` rated PORT-WITH-CHANGES, never ported. 5-axis
  self-rating: accuracy, completeness, clarity, actionability, +1.
- SessionEnd trigger PROVEN for Claude (X5, ledger S19); Copilot UNVERIFIABLE (S4).

## Turn log

### 00:12 — build start
- **Intended:** canonical persona templates, installer seeding, AGENTS.md §8,
  self-review skill, hook cadence note.
- **Tried:** worktree off ce0edbe; read adapters.py, AGENTS.md, ledger, hooks.
- **Happened:** built and committed as 7220a9f — canonical/persona/{SOUL,IDENTITY}.md,
  adapters install_persona() (seed-if-absent, never overwrite), AGENTS.md Persona
  imports + §8, canonical skill self-review, session-end hook cadence note, README.
  Install verified twice: persona seeded; agent-edited SOUL.md untouched on re-install.

### 00:19–00:26 — load probe (worker A)
- **Intended:** prove SOUL content reaches a live session via the shipped shape.
- **Happened:** PROVEN — marker reproduced verbatim via the `@SOUL.md` import
  (Claude 2.1.285, Haiku); negative control NOT LOADED; dangling imports do not
  break AGENTS.md load. $0.0495. Evidence: evals/results/2026-10-01-S25-soul-load-probe.md.

### 00:19–00:36 — behavior probe run 1 (worker B)
- **Intended:** seeded-friction session → protocol-conformant self-update.
- **Happened:** PARTIAL — routing, persona bar, 5-axis entry, wiki log, and
  `self-review: 2026-10-01` commit all fired; lessons were generic (seeded
  `demo/` fact dropped) and cited no session file. $0.0992.
  Evidence: evals/results/2026-10-01-S25-self-review-behavior-probe.md.

### 00:38 — fix + rerun (coordinator)
- **Intended:** close the two run-1 failures in the skill text, re-probe.
- **Tried:** mechanism rule + pre-commit conformance checklist in the skill,
  §8 Lessons format tightened (commit e724470); identical fixture rerun.
- **Happened:** PROVEN 5/5 — mechanism named (`demo/` vs repo root), exact
  session-file citations, SOUL.md md5 unchanged, one commit. Exit 0,
  $0.1232, 17 turns. Evidence: evals/results/2026-10-01-S25-self-review-rerun.md.

## Learned
- Claude Code expands `@path` imports inside a natively loaded AGENTS.md;
  a dangling import (target absent) is tolerated — the base file still loads.
- A self-review protocol's mechanics (routing, commit) are the easy half;
  lesson *content* conformance (mechanism, exact citation) needs an explicit
  rule plus a pre-commit checklist in the skill, or the agent paraphrases.
- Persona ownership and installer idempotence compose: seed-if-absent is the
  only safe installer semantics for agent-owned files.

## Outcome
complete — pattern shipped on feat/soul-self-review; ledger S25 PROVEN
(Claude scope; Copilot cadence UNVERIFIED). Total metered spend $0.2718 of
$3 cap. Open: Copilot-side behavioral run of the protocol (untested);
IDENTITY.md import not separately probed (mechanism proven via SOUL arm).
