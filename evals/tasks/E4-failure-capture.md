# E4 — Failure capture

**Claim S4:** Concrete tool failures land in the sidecar as structured events, 
in both tools, without polluting the prompt.

**Pre-registered threshold:** PASS if ≥ 4/5 induced failures produce a 
parseable JSONL event in `wiki/telemetry/events.jsonl` with timestamp + kind, 
per tool.

## Induced failures (deterministic)
1. `python` (not `python3`) invocation on a python3-only box
2. Nonexistent file read
3. Failing test run
4. Invalid JSON edit
5. Command with exit code 2

## Notes
- Hook delivery semantics differ per tool (blocking vs async, payload shape). 
  Record the actual payload per tool — that diff is adapter requirements, 
  not an excuse.
- If a tool cannot fire hooks on failure, the fallback (PostToolUse exit-code 
  check) must be documented and re-tested.
