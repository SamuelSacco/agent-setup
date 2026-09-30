# E4 backup — the 5 events that landed in wiki/telemetry/events.jsonl (Claude)

All 5 induced failures, captured via `PostToolUseFailure` → sidecar:

```
2026-09-30T05:15:57Z tool_failure | Bash | Exit code 127 (eval):1: command not found: python
2026-09-30T05:15:59Z tool_failure | Bash | Exit code 1 cat: ./no-such-file-xyz.txt: No such file or directory
2026-09-30T05:16:01Z tool_failure | Bash | Exit code 1 E ======== (unittest import error)
2026-09-30T05:16:03Z tool_failure | Bash | Exit code 1 Expecting property name enclosed in double quotes (bad JSON)
2026-09-30T05:16:04Z tool_failure | Bash | Exit code 2
```

Before the adapter fix the same run captured 0 — `PostToolUse` is success-only.
Copilot CLI v1.0.89 captured 0/5 failures as wired. Corrected mechanism
(E4 addendum): hooks load in trusted dirs and sessionStart/preToolUse/
postToolUse fire; postToolUseFailure does not fire for shell failures
(the shell tool reports success on non-zero exit). Full write-up:
`evals/results/2026-09-30-E4.md`.
