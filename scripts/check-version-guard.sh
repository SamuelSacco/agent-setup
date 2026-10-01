#!/usr/bin/env bash
# check-version-guard.sh — X19 version guard for the shared AGENTS.md setup.
#
# Fails (exit 1) when any of these invariants breaks:
#   (1) Version floor — installed Claude Code < 2.1.277, the first version
#       that loads AGENTS.md natively. Checked unconditionally (unlike
#       scripts/check-agents-md-load.sh, which waives the floor when a
#       bridged CLAUDE.md is present).
#   (2) Bridge invariant — any CLAUDE.md anywhere in the target tree
#       (excluding .git/) that does not contain the `@AGENTS.md` bridge
#       line. An annex-only CLAUDE.md suppresses the native AGENTS.md
#       read (proven 2/2, evals/results/2026-09-30-P2-claudemd-drop.md).
#   (3) Marker load — the AGENTS.md marker sentence is present in the
#       file, and (unless --skip-live) a headless Claude session started
#       in a scratch copy of the tree's instruction files actually loads
#       it (marker-probe, same approach as check-agents-md-load.sh).
#
# Usage:
#   scripts/check-version-guard.sh [--root DIR] [--skip-live] [--live-only] [--runs N]
#     --root DIR    tree to check (default: this repo's root)
#     --skip-live   static checks only (1)+(2)+(3-static); offline, $0
#     --live-only   live marker probe only (negative-control testing)
#     --runs N      live probes to run (default 1)
#
# Env:
#   CLAUDE_BIN              claude binary override (also the test seam:
#                           point it at a shim printing an old version
#                           to exercise check (1) — never downgrade the
#                           real CLI)
#   CLAUDE_API_KEY_HELPER   apiKeyHelper for the live probe
#   VG_TMPDIR               parent dir for the live probe's scratch copy
#                           (default: ${TMPDIR:-/tmp})
#
# Exit codes: 0 = all requested checks pass, 1 = an invariant FAILED,
#             2 = harness error (no claude binary / no key helper /
#                 unparseable probe output — no verdict).
#
# Cost: static mode $0. Each live probe is one Haiku call (~$0.012 at
# 2026-09-30 prices); the probe prints its metered total_cost_usd.
# Evidence: evals/results/2026-10-01-X19-version-guard.md; ledger C4.
set -uo pipefail

SCRIPT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ROOT="$SCRIPT_ROOT"
RUNS=1
DO_STATIC=1
DO_LIVE=1
while [ $# -gt 0 ]; do
  case "$1" in
    --root) ROOT="$2"; shift 2 ;;
    --runs) RUNS="$2"; shift 2 ;;
    --skip-live|--static) DO_LIVE=0; shift ;;
    --live-only|--skip-static) DO_STATIC=0; shift ;;
    *) echo "check-version-guard: unknown arg: $1" >&2; exit 2 ;;
  esac
done
ROOT="$(cd "$ROOT" && pwd)"

MARKER='Orientation is what makes the wiki compound'
MARKER_TAIL='makes the wiki compound'
FLOOR='2.1.277'
MODEL='claude-haiku-4-5-20251001'
HELPER="${CLAUDE_API_KEY_HELPER:-$HOME/workspace/skills/anthropic/bin/claude_api_key_helper.py}"

fail() { echo "FAIL: $1"; exit 1; }
herr() { echo "ERROR: $1" >&2; exit 2; }
pass() { echo "PASS: $1"; }

claude_bin() {
  if [ -n "${CLAUDE_BIN:-}" ]; then echo "$CLAUDE_BIN";
  elif [ -x "$HOME/workspace/tools/bin/claude" ]; then echo "$HOME/workspace/tools/bin/claude";
  elif command -v claude >/dev/null 2>&1; then command -v claude;
  else return 1; fi
}

# First semver in the string, leading v stripped; tolerates
# "2.1.285 (Claude Code)", "v2.1.285", "claude version 2.1.285".
parse_version() {
  printf '%s' "$1" | grep -oE 'v?[0-9]+\.[0-9]+\.[0-9]+' | head -n1 | sed 's/^v//'
}

version_lt() { # $1 < $2 ?
  [ "$1" != "$2" ] && [ "$(printf '%s\n%s\n' "$1" "$2" | sort -V | head -n1)" = "$1" ]
}

[ -f "$ROOT/AGENTS.md" ] || fail "no AGENTS.md in $ROOT — nothing to guard"

if [ "$DO_STATIC" -eq 1 ]; then
  # (1) version floor — unconditional
  CB="$(claude_bin)" || herr "(1) no claude binary found (set CLAUDE_BIN) — cannot verify the version floor"
  RAW_VER="$("$CB" --version 2>/dev/null)" || herr "(1) '$CB --version' failed — cannot verify the version floor"
  VER="$(parse_version "$RAW_VER")"
  [ -n "$VER" ] || herr "(1) could not parse a version from: $RAW_VER"
  if version_lt "$VER" "$FLOOR"; then
    fail "(1) Claude Code $VER < $FLOOR — native AGENTS.md load requires >= $FLOOR; upgrade Claude Code"
  fi
  pass "(1) Claude Code $VER >= floor $FLOOR"

  # (2) every CLAUDE.md in the tree must carry the bridge
  CLAUDE_FILES=()
  while IFS= read -r -d '' cmd_file; do
    CLAUDE_FILES+=("$cmd_file")
  done < <(find "$ROOT" -name 'CLAUDE.md' -not -path '*/.git/*' -type f -print0 | sort -z)
  if [ "${#CLAUDE_FILES[@]}" -eq 0 ]; then
    pass "(2) no CLAUDE.md in $ROOT — nothing can suppress the native AGENTS.md read"
  fi
  for cmd_file in "${CLAUDE_FILES[@]}"; do
    if grep -qE '^@AGENTS\.md[[:space:]]*$' "$cmd_file"; then
      pass "(2) $cmd_file carries the @AGENTS.md bridge"
    else
      fail "(2) $cmd_file exists WITHOUT the @AGENTS.md bridge line — it suppresses the native AGENTS.md read; add the bridge line or delete the file"
    fi
  done

  # (3-static) marker present in AGENTS.md
  grep -qF "$MARKER" "$ROOT/AGENTS.md" \
    || fail "(3) marker sentence not found in $ROOT/AGENTS.md — the shared file no longer carries the load marker"
  pass "(3) AGENTS.md marker present in $ROOT/AGENTS.md"
fi

if [ "$DO_LIVE" -eq 1 ]; then
  CB="$(claude_bin)" || herr "(3) no claude binary found (set CLAUDE_BIN) — cannot run the live probe"
  [ -f "$HELPER" ] || herr "(3) apiKeyHelper not found at $HELPER (set CLAUDE_API_KEY_HELPER) — cannot authenticate the live probe"
  TMPBASE="${VG_TMPDIR:-${TMPDIR:-/tmp}}"
  mkdir -p "$TMPBASE"
  TMP="$(mktemp -d "$TMPBASE/version-guard.XXXXXX")"
  trap 'rm -rf "$TMP"' EXIT
  PROJ="$TMP/project"
  mkdir -p "$PROJ/.claude"
  cp "$ROOT/AGENTS.md" "$PROJ/AGENTS.md"
  [ -f "$ROOT/CLAUDE.md" ] && cp "$ROOT/CLAUDE.md" "$PROJ/CLAUDE.md"
  printf '{"apiKeyHelper": "%s"}\n' "$HELPER" > "$PROJ/.claude/settings.json"
  PROMPT='From the project instructions loaded at session start: reproduce exactly, on a single line, the sentence that explains why orientation matters — it ends with the words "wiki compound". If no such sentence was in your loaded instructions, reply with exactly: NOT LOADED. Use no tools.'
  i=1
  while [ "$i" -le "$RUNS" ]; do
    OUT="$TMP/out$i.json"
    ( cd "$PROJ" && HOME="$TMP/home$i" "$CB" -p "$PROMPT" --model "$MODEL" \
        --output-format json > "$OUT" 2>/dev/null )
    RESULT="$(python3 -c 'import json,sys
try:
    d=json.load(open(sys.argv[1])); print(d.get("result") or "")
except Exception:
    sys.exit(3)' "$OUT")" || herr "(3) probe run $i produced unparseable output — harness error, no verdict"
    COST="$(python3 -c 'import json,sys
try:
    print(json.load(open(sys.argv[1])).get("total_cost_usd") or "")
except Exception:
    print("")' "$OUT")"
    if printf '%s' "$RESULT" | grep -qF "$MARKER_TAIL"; then
      pass "(3) live probe $i/$RUNS: AGENTS.md marker loaded (metered cost_usd=${COST:-unreported})"
    else
      fail "(3) live probe $i/$RUNS: marker NOT loaded — AGENTS.md did not reach the session (metered cost_usd=${COST:-unreported}). Probe said: $(printf '%s' "$RESULT" | head -c 200)"
    fi
    i=$((i + 1))
  done
fi

echo "check-version-guard: all requested checks passed for $ROOT"
exit 0
