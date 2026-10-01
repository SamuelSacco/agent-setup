# S25 — SOUL load probe

Date: 2026-10-01, runs 00:19–00:26 EDT.
Question: does `SOUL.md` content reach a live Claude session via the shipped shape — root `AGENTS.md` Persona section carrying `@SOUL.md` / `@IDENTITY.md` import lines, no `CLAUDE.md`?
Overall verdict: **PROVEN**.

## Setup

- Source: local clone `~/workspace/w2-soul` → `~/workspace/w2-probe-load`, branch `feat/soul-self-review`, commit `7220a9f`. No network clone (GitHub flaky).
- Markers, verified in source before running:
  - SOUL marker (`SOUL.md`): "A persona edit that is not a diffable commit did not happen."
  - AGENTS guard marker (`AGENTS.md` §1): "Orientation is what makes the wiki compound."
- Harness: pattern copied from `scripts/check-agents-md-load.sh`. Binary `~/workspace/tools/bin/claude` (2.1.285, ≥ floor 2.1.277). Model `claude-haiku-4-5-20251001`. Per-arm fresh consumer project under `~/workspace/w2-probe-load-scratch/<arm>/project` with `.claude/settings.json` = `{"apiKeyHelper": "/home/hatch/workspace/skills/anthropic/bin/claude_api_key_helper.py"}`, per-arm scratch `HOME`, `--output-format json`, no tools (prompt instruction only).
- Confound check: every debug log also lists ancestor `/home/hatch/AGENTS.md` as loaded. That file contains neither marker (grep count 0/0), so it cannot explain a marker hit.
- Network: Anthropic API connection errors during Arm 1 (5 retries logged) and Arm 2 (1 retry). All runs completed `is_error: false`, `num_turns: 1`. Arm 1 `duration_ms` 319556 is retry time, not load time.

## Arm 1 — full shape

- Project shape: `AGENTS.md` + `SOUL.md` + `IDENTITY.md` + `.claude/settings.json`.
- Prompt: `From the project instructions loaded at session start: reproduce exactly the sentence in your persona file about persona edits and commits — it contains the words "diffable commit". If no such sentence was in your loaded instructions, reply with exactly: NOT LOADED. Use no tools.`
- Result (verbatim): `A persona edit that is not a diffable commit did not happen.`
- Cost: $0.01638115.
- Debug log: `no CLAUDE.md found; AGENTS.md loaded: /home/hatch/AGENTS.md, /home/hatch/workspace/w2-probe-load-scratch/arm1/project/AGENTS.md`.
- Verdict: **PASS**. SOUL.md content, reachable only through the `@SOUL.md` import in AGENTS.md (the file itself is not an instruction file Claude loads natively), was in the session's loaded instructions.

## Arm 2 — negative control (SOUL.md deleted)

- Project shape: `AGENTS.md` + `IDENTITY.md` + `.claude/settings.json`. `SOUL.md` absent; the `@SOUL.md` import dangles.
- Prompt: identical to Arm 1.
- Result (verbatim): `NOT LOADED`
- Cost: $0.0159599.
- Verdict: **PASS (control clean)**. No false load: the marker appears only when SOUL.md is present. Arm 1's hit is attributable to the import, not to model prior knowledge or guessing.

## Arm 3 — missing-import target (AGENTS.md alone)

- Project shape: `AGENTS.md` + `.claude/settings.json`. Both persona files absent; both imports dangle.
- Prompt: `From the project instructions loaded at session start: reproduce exactly, on a single line, the sentence that explains why orientation matters — it ends with the words "wiki compound". If no such sentence was in your loaded instructions, reply with exactly: NOT LOADED. Use no tools.`
- Result (verbatim): `Orientation is what makes the wiki compound.`
- Cost: $0.01712115.
- Verdict: **PASS**. A dangling `@SOUL.md` / `@IDENTITY.md` import does not break the AGENTS.md load. The repo's existing guard probe (`check-agents-md-load.sh`, which copies AGENTS.md alone) remains valid on this branch.

## Arm 4 — not run

Optional IDENTITY-specific probe. Arms 1–3 are unambiguous (marker present iff file present; AGENTS loads with dangling imports), so no further spend was justified. Whether `@IDENTITY.md` specifically expands is not separately proven by this probe; Arm 1 proves the import mechanism for the first import line only.

## Totals

- Spend: $0.01638115 + $0.0159599 + $0.01712115 = **$0.0494622** (cap $1).
- Raw outputs: `~/workspace/w2-probe-load-scratch/arm{1,2,3}/out.json`, `debug.log` per arm.

## Verdict

**PROVEN** — in the shipped shape (AGENTS.md + Persona `@` imports, no CLAUDE.md), SOUL.md content loads into a live Claude Code session at start. Mechanism: native AGENTS.md load (Claude 2.1.285) expanding the `@SOUL.md` import; evidenced by Arm 1 hit, Arm 2 clean control, Arm 3 showing dangling imports do not break the base load.
