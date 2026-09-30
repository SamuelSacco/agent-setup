---
id: session-end-hook
title: Claim — a session-end hook fires automatically at session close in Claude Code (headless included)
type: claim
status: active
created: 2026-09-30
updated: 2026-09-30
verified: 2026-09-30
relates_to: [session-lifecycle, telemetry-storage]
sources: []
tags: [hooks, session-end, claude-code]
verdict: PROVEN (trigger, Claude only)
evidence: evals/results/2026-09-30-X5-sessionend-probe.md
---

Ledger S18. Tested 2026-09-30 (backlog X5): on Claude Code 2.1.285, a
hook registered on the `SessionEnd` event fired at the end of headless
`claude -p` sessions — 2/2 in a scratch probe (marker written by the
hook alone, distinct session ids matching the CLI's) and 1/1 through
the shipped wiring: canonical `session_end` event →
`.claude/settings.json` → `./scripts/sidecar.sh record-session-end` →
`kind: "session_end"` line in `wiki/telemetry/events.jsonl`.

Scoped precisely: the **trigger** is proven; a cleanup *skill* is not —
the wired action is a sidecar record, the stub cleanup steps attach to.
The probe sessions' model turns failed on exhausted API credit ($0
metered) and still terminated via the normal lifecycle
(`reason: "other"`), hook firing each time. Copilot: UNVERIFIABLE —
the installed CLI has no hook loader (S4); the adapter emits the
`sessionEnd` file for when it ships one.
