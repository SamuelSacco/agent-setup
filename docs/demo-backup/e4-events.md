# E4 backup — the 5 events that landed in wiki/telemetry/events.jsonl (Claude)

Note (2026-10-01): the events shown below were captured 2026-09-30,
pre-amendment, under the old raw-payload format. They are the historical
capture, not the current store format — see the S4 amendment section at
the end of this file.

All 5 induced failures, captured via `PostToolUseFailure` → sidecar:

```
2026-09-30T05:15:57Z tool_failure | Bash | Exit code 127 (eval):1: command not found: python
2026-09-30T05:15:59Z tool_failure | Bash | Exit code 1 cat: ./no-such-file-xyz.txt: No such file or directory
2026-09-30T05:16:01Z tool_failure | Bash | Exit code 1 E ======== (unittest import error)
2026-09-30T05:16:03Z tool_failure | Bash | Exit code 1 Expecting property name enclosed in double quotes (bad JSON)
2026-09-30T05:16:04Z tool_failure | Bash | Exit code 2
```

Before the adapter fix the same run captured 0 — `PostToolUse` is success-only.
Copilot CLI v1.0.89 captured 0/5 failures as wired — scope: that was the
untrusted-dir observation. Current ledger verdict (S4) is
PARTIAL-with-mechanism: hooks fire under trust / `COPILOT_ALLOW_ALL=true`;
`postToolUseFailure` never fires for shell failures (the shell tool
reports success on non-zero exit). Corrected mechanism
(E4 addendum): hooks load in trusted dirs and sessionStart/preToolUse/
postToolUse fire; postToolUseFailure does not fire for shell failures
(the shell tool reports success on non-zero exit). Full write-up:
`evals/results/2026-09-30-E4.md`.

## S4 amendment — telemetry redaction (ledger S4 AMENDMENT, 2026-09-30; branch `fix/adapter-tools-telemetry`)

The sidecar no longer stores raw payloads. Current format is allowlist
only: `ts`, `kind`, `tool`, `event`, and the error first line (≤120
chars). `tool_input`, `tool_response`, and paths are never written.
Malformed stdin yields one valid line (`error_class: malformed_payload`)
instead of corrupting the store. `wiki/telemetry/` is gitignored and
`events.jsonl` is untracked (it was previously committed with raw
payloads).
