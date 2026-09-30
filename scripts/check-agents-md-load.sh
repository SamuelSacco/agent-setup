#!/usr/bin/env bash
# check-agents-md-load.sh — guard for the no-CLAUDE.md final shape.
#
# This repo ships ONE shared instruction file, AGENTS.md, and no CLAUDE.md.
# That is safe only while three invariants hold; this script fails (exit 1)
# if any of them breaks:
#
#   (a) Version floor — if CLAUDE.md is absent, the installed Claude Code
#       must be >= 2.1.277 (first version that loads AGENTS.md natively).
#   (b) Bridge invariant — if a CLAUDE.md (re)appears, its content must
#       include the `@AGENTS.md` import line. An annex-only CLAUDE.md
#       silently SUPPRESSES the native AGENTS.md read in the default
#       memory mode (proven, W5 arm C: evals/results/
#       2026-09-30-P2-claudemd-drop.md).
#   (c) Live load — the shared marker sentence in AGENTS.md must actually
#       reach a live Claude session started in a consumer project built
#       from this tree's instruction files.
#
# Usage:
#   scripts/check-agents-md-load.sh [--root DIR] [--runs N]
#                                   [--static] [--skip-static] [--skip-live]
#     --root DIR     tree to check (default: this repo's root)
#     --runs N       live probes to run (default 1; proof runs use 2)
#     --static       static checks only (a)+(b) — the run-eval preflight mode
#     --skip-static  live probe only (negative-control testing)
#     --skip-live    same as --static
#
# Exit codes: 0 = all checks pass, 1 = an invariant FAILED,
#             2 = harness error (no claude binary / no key helper /
#                 unparseable probe output — no verdict on the invariants).
#
# Cost: static mode is free. Each live probe is one Haiku call (~$0.011
# at 2026-09-30 prices, default context). Evidence for the invariants:
# evals/results/2026-09-30-P2-claudemd-final-shape.md (ledger claim C4).
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
    --static|--skip-live) DO_LIVE=0; shift ;;
    --skip-static) DO_STATIC=0; shift ;;
    *) echo "check-agents-md-load: unknown arg: $1" >&2; exit 2 ;;
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

version_lt() { # $1 < $2 ?
  [ "$(printf '%s\n%s\n' "$1" "$2" | sort -V | head -n1)" != "$2" ]
}

[ -f "$ROOT/AGENTS.md" ] || fail "no AGENTS.md in $ROOT — nothing to guard"
grep -qF "$MARKER" "$ROOT/AGENTS.md" \
  || fail "marker sentence not found in $ROOT/AGENTS.md (guard marker drifted from the file)"
pass "AGENTS.md present in $ROOT with guard marker"

CLAUDE_MD_PRESENT=0
[ -f "$ROOT/CLAUDE.md" ] && CLAUDE_MD_PRESENT=1

if [ "$DO_STATIC" -eq 1 ]; then
  if [ "$CLAUDE_MD_PRESENT" -eq 1 ]; then
    if grep -qE '^@AGENTS\.md[[:space:]]*$' "$ROOT/CLAUDE.md"; then
      pass "(b) CLAUDE.md present and carries the @AGENTS.md bridge"
    else
      fail "(b) $ROOT/CLAUDE.md exists WITHOUT the @AGENTS.md bridge — it suppresses the native AGENTS.md read; add the bridge line or delete the file"
    fi
  else
    pass "(b) no CLAUDE.md — nothing can suppress the native AGENTS.md read"
    CB="$(claude_bin)" || herr "(a) no claude binary found (set CLAUDE_BIN) — cannot verify the version floor"
    VER="$("$CB" --version | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -n1)"
    [ -n "$VER" ] || herr "(a) could not parse a version from: $CB --version"
    if version_lt "$VER" "$FLOOR"; then
      fail "(a) Claude Code $VER < $FLOOR and CLAUDE.md is absent — AGENTS.md would NOT load natively; restore the @AGENTS.md bridge file or upgrade Claude Code"
    fi
    pass "(a) Claude Code $VER >= floor $FLOOR with CLAUDE.md absent"
  fi
fi

if [ "$DO_LIVE" -eq 1 ]; then
  CB="$(claude_bin)" || herr "(c) no claude binary found (set CLAUDE_BIN) — cannot run the live probe"
  [ -f "$HELPER" ] || herr "(c) apiKeyHelper not found at $HELPER (set CLAUDE_API_KEY_HELPER) — cannot authenticate the live probe"
  TMP="$(mktemp -d /tmp/agentsmd-guard.XXXXXX)"
  trap 'rm -rf "$TMP"' EXIT
  PROJ="$TMP/project"
  mkdir -p "$PROJ/.claude"
  cp "$ROOT/AGENTS.md" "$PROJ/AGENTS.md"
  [ "$CLAUDE_MD_PRESENT" -eq 1 ] && cp "$ROOT/CLAUDE.md" "$PROJ/CLAUDE.md"
  printf '{"apiKeyHelper": "%s"}\n' "$HELPER" > "$PROJ/.claude/settings.json"
  PROMPT='From the project instructions loaded at session start: reproduce exactly, on a single line, the sentence that explains why orientation matters — it ends with the words "wiki compound". If no such sentence was in your loaded instructions, reply with exactly: NOT LOADED. Use no tools.'
  i=1
  while [ "$i" -le "$RUNS" ]; do
    OUT="$TMP/out$i.json"
    ( cd "$PROJ" && HOME="$TMP/home$i" "$CB" -p "$PROMPT" --model "$MODEL" \
        --output-format json --debug-file "$TMP/debug$i.log" > "$OUT" 2>/dev/null )
    RESULT="$(python3 -c 'import json,sys
try:
    print(json.load(open(sys.argv[1])).get("result") or "")
except Exception:
    sys.exit(3)' "$OUT")" || herr "(c) probe run $i produced unparseable output — harness error, no verdict"
    if printf '%s' "$RESULT" | grep -qF "$MARKER_TAIL"; then
      LOADER="loader line not captured"
      grep -q 'AGENTS.md loaded' "$TMP/debug$i.log" 2>/dev/null && LOADER="debug log confirms AGENTS.md loaded"
      pass "(c) live probe $i/$RUNS: AGENTS.md marker loaded ($LOADER)"
    else
      fail "(c) live probe $i/$RUNS: marker NOT in session output — AGENTS.md did not load in the final tree shape. Probe said: $(printf '%s' "$RESULT" | head -c 200)"
    fi
    i=$((i + 1))
  done
fi

echo "check-agents-md-load: all requested checks passed for $ROOT"
exit 0
