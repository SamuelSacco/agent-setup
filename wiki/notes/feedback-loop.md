---
id: feedback-loop
title: The Feedback Loop — Capture, Review, Judge, Improve
type: procedure
status: active
created: 2026-09-30
updated: 2026-09-30
verified: 2026-09-30
relates_to: [session-lifecycle, telemetry-storage]
tags: [feedback-loop, evals, claims-ledger]
---

# The feedback loop

Full adopter-facing procedure: `docs/feedback-loop.md`. The loop in one
paragraph: sessions leave records (`wiki/sessions/`) and failure events
(`wiki/telemetry/events.jsonl`); at close, the session-harden skill
distills them into notes; claims about the system live in
`docs/claims-ledger.md` and earn PROVEN / REFUTED / UNVERIFIABLE only
from evals graded on disk; a refuted claim drives a fix in `canonical/`,
a re-run of `./scripts/install.sh`, and a re-run of the eval.

The eval step is a shipped tool, not scratch code: `scripts/run-eval.sh`
runs a task package from `evals/tasks-packaged/<id>/` (task.json +
prompt.txt + requirements.txt) — parent-commit export, fresh git init,
headless tool run, fix-commit tests overlaid, pytest executed by the
runner, results file with cost/turns and a verdict line. Proven
end-to-end 2026-09-30 (ledger S16): nx-t2 package, claude/base, PASS,
11 turns, $0.103 metered.

Honest labels, kept current in the doc: capture is automatic only where
the tool delivers hook events (Copilot partial, S4); session-harden and
ledger updates are agent-run; no scheduler, collector, or dashboard is
shipped — files are the store ([[telemetry-storage]]).
