#!/usr/bin/env bash
# Sidecar collector: structured telemetry OUTSIDE the prompt context.
#
# Why not Postgres? Events are append-only, single-writer, low volume, and the
# consumers are agents reading files. JSONL + sqlite-utils/jq covers it.
# Graduate to Postgres only if: multiple concurrent writers, cross-machine
# queries, or retention/search outgrows flat files. (Decision note: see
# wiki note `telemetry-storage`.)
#
# PRIVACY RULE (critique 2026-09-30, Pass 4 HIGH #3): hook payloads carry
# tool_input — full shell commands, file contents on failed writes. The raw
# payload is NEVER written to disk. record-* extracts an allowlist of fields
# only (see the inline extractor below), and wiki/telemetry/ is gitignored:
# events stay local, never committed.
#
# Usage:
#   sidecar.sh record-failure     # reads a JSON event on stdin, appends an allowlisted line
#   sidecar.sh record-session-end # same, for SessionEnd hook payloads (X5/S19)
#   sidecar.sh summary [date]     # prints a compact summary (safe for prompts)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
STORE="$ROOT/wiki/telemetry"
mkdir -p "$STORE"
EVENTS="$STORE/events.jsonl"
touch "$EVENTS"

record_event() {
  # $1 = kind. Reads the raw hook payload on stdin, appends ONE JSON line
  # containing only allowlisted fields. Non-JSON input still yields exactly
  # one valid JSON line (kind + malformed marker), never a raw insert.
  local kind="$1" tmp
  tmp="$(mktemp "$STORE/.payload.XXXXXX")"
  cat > "$tmp" || true
  python3 - "$EVENTS" "$kind" "$tmp" <<'PYEOF'
import json
import sys
from datetime import datetime, timezone

events_path, kind, payload_path = sys.argv[1], sys.argv[2], sys.argv[3]
with open(payload_path, encoding="utf-8", errors="replace") as f:
    raw = f.read()

line = {"ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "kind": kind}

try:
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise ValueError("payload is not a JSON object")
except Exception:
    line["valid"] = False
    line["error_class"] = "malformed_payload"
else:
    def short_str(v, limit):
        return v[:limit] if isinstance(v, str) else None

    # Allowlist — Claude Code hook payload fields (PostToolUseFailure /
    # SessionEnd). tool_input, tool_response, transcript_path, cwd and any
    # other field are dropped by construction: they are never copied.
    tool = short_str(data.get("tool_name"), 80)
    if tool is not None:
        line["tool"] = tool
    event = short_str(data.get("hook_event_name"), 40)
    if event is not None:
        line["event"] = event
    if kind == "tool_failure":
        err = data.get("error")
        if isinstance(err, str) and err.strip():
            # Error class only: first line, truncated. Never the full text.
            line["error_class"] = err.strip().splitlines()[0][:120]
        if isinstance(data.get("is_interrupt"), bool):
            line["is_interrupt"] = data["is_interrupt"]
    if kind == "session_end":
        sid = short_str(data.get("session_id"), 64)
        if sid is not None:
            line["session_id"] = sid
        reason = short_str(data.get("reason"), 40)
        if reason is not None:
            line["reason"] = reason

with open(events_path, "a", encoding="utf-8") as f:
    f.write(json.dumps(line, separators=(",", ":")) + "\n")
PYEOF
  rm -f "$tmp"
}

case "${1:-}" in
  record-failure)
    record_event "tool_failure"
    ;;
  record-session-end)
    # SessionEnd hook payload (session_id, reason, cwd, transcript_path).
    # The record itself is the cleanup stub: session-close steps attach
    # here. Trigger PROVEN headless in Claude Code 2.1.285 (X5, S19).
    # Only session_id + reason are recorded (allowlist, see header).
    record_event "session_end"
    ;;
  summary)
    day="${2:-$(date -u +%F)}"
    echo "Telemetry $day: $(grep -c "\"ts\":\"$day" "$EVENTS" 2>/dev/null || true) events"
    grep "^{\"ts\":\"$day" "$EVENTS" 2>/dev/null \
      | python3 -c 'import sys,json,collections
c=collections.Counter()
for line in sys.stdin:
    try: c[json.loads(line).get("kind","?")]+=1
    except Exception: pass
for k,v in c.most_common(): print(f"  {k}: {v}")' || true
    ;;
  *)
    echo "usage: sidecar.sh record-failure|record-session-end|summary [date]" >&2; exit 2 ;;
esac
