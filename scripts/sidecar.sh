#!/usr/bin/env bash
# Sidecar collector: structured telemetry OUTSIDE the prompt context.
#
# Why not Postgres? Events are append-only, single-writer, low volume, and the
# consumers are agents reading files. JSONL + sqlite-utils/jq covers it.
# Graduate to Postgres only if: multiple concurrent writers, cross-machine
# queries, or retention/search outgrows flat files. (Decision note: see
# wiki note `telemetry-storage`.)
#
# Usage:
#   sidecar.sh record-failure     # reads a JSON event on stdin, appends to store
#   sidecar.sh record-session-end # same, for SessionEnd hook payloads (X5/S18)
#   sidecar.sh summary [date]     # prints a compact summary (safe for prompts)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
STORE="$ROOT/wiki/telemetry"
mkdir -p "$STORE"
EVENTS="$STORE/events.jsonl"
touch "$EVENTS"

case "${1:-}" in
  record-failure)
    ts="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    payload="$(cat || true)"
    printf '{"ts":"%s","kind":"tool_failure","payload":%s}\n' \
      "$ts" "${payload:-null}" >> "$EVENTS"
    ;;
  record-session-end)
    # SessionEnd hook payload (session_id, reason, cwd, transcript_path).
    # The record itself is the cleanup stub: session-close steps attach
    # here. Trigger PROVEN headless in Claude Code 2.1.285 (X5, S18).
    ts="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    payload="$(cat || true)"
    printf '{"ts":"%s","kind":"session_end","payload":%s}\n' \
      "$ts" "${payload:-null}" >> "$EVENTS"
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
