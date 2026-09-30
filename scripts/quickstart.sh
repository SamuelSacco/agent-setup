#!/usr/bin/env bash
# quickstart.sh — one command from a stranger's machine to a verified
# dual-tool (Claude Code + GitHub Copilot CLI) agent-setup workspace.
#
#   git clone <this-repo> agent-setup && cd agent-setup && ./scripts/quickstart.sh
#
# What it does, in order:
#   1. Preflight   — git, python3 present; claude/copilot CLIs present
#                    (npm-installs them into ~/.local if missing and npm exists).
#   2. Workspace   — if run outside a clone, clones the repo; then runs
#                    scripts/install.sh (canonical/ -> both tools' layouts).
#   3. Structural  — verifies materialized counts match canonical/ for BOTH
#      verify        tools and both MCP configs parse. Free, deterministic.
#   4. Auth gate   — if a tool is unauthenticated, prints the exact login
#                    command and exits 2. Re-run quickstart after logging in;
#                    every step is idempotent.
#   5. Live verify — one headless probe per tool asking a question whose
#                    answer exists only in an installed skill's body.
#                    PASS requires the body facts, not the skill name.
#
# Flags: --structural-only   skip live probes (no auth, no API spend)
#        --dir <path>        workspace location when cloning (default ./agent-setup)
#        --repo <url>        repo to clone (default: GitHub URL below)
# Env:   AGENT_SETUP_MODEL   probe model (default claude-haiku-4-5-20251001)
set -uo pipefail

REPO_URL="${AGENT_SETUP_REPO:-https://github.com/SamuelSacco/agent-setup}"
MODEL="${AGENT_SETUP_MODEL:-claude-haiku-4-5-20251001}"
TARGET_DIR="./agent-setup"
LIVE=1

while [ $# -gt 0 ]; do
  case "$1" in
    --structural-only) LIVE=0 ;;
    --dir) TARGET_DIR="$2"; shift ;;
    --repo) REPO_URL="$2"; shift ;;
    *) echo "unknown flag: $1" >&2; exit 64 ;;
  esac
  shift
done

say()  { printf '%s\n' "$*"; }
fail() { printf 'FAIL: %s\n' "$*" >&2; exit 1; }

# ---------------------------------------------------------------- 1. preflight
say "== preflight =="
command -v git     >/dev/null || fail "git not found. Install git, then re-run."
command -v python3 >/dev/null || fail "python3 not found (install.sh needs it). Install Python 3, then re-run."
command -v node    >/dev/null || say "WARN: node not found — MCP servers (npx-based) will not start."
command -v npx     >/dev/null || say "WARN: npx not found — MCP servers (npx-based) will not start."

ensure_cli() { # $1 = binary, $2 = npm package
  if command -v "$1" >/dev/null; then say "found: $1 ($(command -v "$1"))"; return 0; fi
  if command -v npm >/dev/null; then
    say "installing $1 via npm into ~/.local (no sudo)..."
    NPM_LOG="$(mktemp)"
    if ! npm install -g "$2" --prefix "$HOME/.local" >"$NPM_LOG" 2>&1; then
      tail -5 "$NPM_LOG" >&2; rm -f "$NPM_LOG"
      fail "npm install of $2 failed (npm output above). Install $1 manually (see docs/toolchain.md), then re-run."
    fi
    rm -f "$NPM_LOG"
    export PATH="$HOME/.local/bin:$PATH"
    command -v "$1" >/dev/null || fail "$1 installed but not on PATH. Add ~/.local/bin to PATH, then re-run."
    say "installed: $1 -> $HOME/.local/bin/$1 (add ~/.local/bin to your shell PATH permanently)"
  else
    fail "$1 not found and npm unavailable. Install $1 (see docs/toolchain.md), then re-run."
  fi
}
ensure_cli claude  @anthropic-ai/claude-code
ensure_cli copilot @github/copilot

# ---------------------------------------------------------------- 2. workspace
say "== workspace =="
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
if [ -f "$SCRIPT_DIR/install.sh" ] && [ -d "$SCRIPT_DIR/../canonical" ]; then
  ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
  say "using this clone: $ROOT"
else
  if [ -d "$TARGET_DIR/.git" ]; then
    say "using existing clone: $TARGET_DIR"
  else
    say "cloning $REPO_URL -> $TARGET_DIR"
    git clone -q "$REPO_URL" "$TARGET_DIR" || fail "clone failed (private repo? check your access)."
  fi
  ROOT="$(cd "$TARGET_DIR" && pwd)"
fi
cd "$ROOT"
./scripts/install.sh >/dev/null || fail "scripts/install.sh failed."

# ------------------------------------------------------- 3. structural verify
say "== structural verify =="
python3 - <<'PY' || fail "structural verify failed (details above)."
import json, pathlib, sys
root = pathlib.Path(".")
canon_skills = len(list((root/"canonical/skills").glob("*.md")))
canon_agents = len(list((root/"canonical/agents").glob("*.md")))
checks = [
    ("claude skills",  len(list((root/".claude/skills").glob("*/SKILL.md"))), canon_skills),
    ("copilot skills", len(list((root/".github/skills").glob("*/SKILL.md"))), canon_skills),
    ("claude agents",  len(list((root/".claude/agents").glob("*.md"))), canon_agents),
    ("copilot agents", len(list((root/".github/agents").glob("*.agent.md"))), canon_agents),
]
bad = 0
for name, got, want in checks:
    ok = got == want
    bad += not ok
    print(f"{'ok  ' if ok else 'BAD '} {name}: {got}/{want}")
for tool, path, key in (("claude", ".mcp.json", "mcpServers"), ("copilot", ".github/mcp.json", "servers")):
    try:
        servers = json.loads((root/path).read_text())[key]
        print(f"ok   {tool} mcp config parses: {len(servers)} servers")
    except Exception as e:
        bad += 1
        print(f"BAD  {tool} mcp config: {e}")
sys.exit(1 if bad else 0)
PY
say "structural verify: PASS"

# ---------------------------------------------------------------- 4. auth gate
if [ "$LIVE" -eq 0 ]; then
  say "== live verify skipped (--structural-only) =="
  say "Setup materialized but NOT live-verified. Authenticate both tools, then re-run without the flag."
  exit 0
fi
say "== auth gate =="
if ! claude auth status 2>/dev/null | grep -q '"loggedIn": true'; then
  say "Claude Code is not authenticated. Run:  claude auth login"
  say "Then re-run ./scripts/quickstart.sh — completed steps are skipped."
  exit 2
fi
say "claude: authenticated"

# ------------------------------------------------------------- 5. live verify
say "== live verify =="
PROBE="From the session-harden skill's steps and rules: which directory must never be edited, and what are the three allowed final status values for a session file? Answer in one short line."
# NB: read stdin ONCE into a variable — sequential greps on a pipe starve
# (first grep consumes the stream; later greps see EOF and fail).
check_answer() { local t; t="$(cat)"
  grep -qi 'wiki/raw'  <<<"$t" && grep -qi 'complete'  <<<"$t" \
  && grep -qi 'partial' <<<"$t" && grep -qi 'abandoned' <<<"$t"; }

OUT="$(claude -p "$PROBE" --model "$MODEL" --output-format json </dev/null 2>/dev/null)"
RESULT="$(printf '%s' "$OUT" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("result",""))' 2>/dev/null)"
if printf '%s' "$RESULT" | check_answer; then
  COST="$(printf '%s' "$OUT" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("total_cost_usd","?"))' 2>/dev/null)"
  say "claude live probe: PASS (cost \$$COST)"
else
  say "claude probe returned: ${RESULT:-<no parseable result>}" >&2
  fail "claude live probe did not return the skill-body facts. Is the probe model available on your account? Is cwd the repo root?"
fi

OUT="$(copilot -p "$PROBE" --allow-all-tools </dev/null 2>&1)"
if printf '%s' "$OUT" | check_answer; then
  say "copilot live probe: PASS"
elif printf '%s' "$OUT" | grep -qi 'No authentication'; then
  say "Copilot CLI is not authenticated. Run:  copilot login   (or set COPILOT_GITHUB_TOKEN)"
  say "Then re-run ./scripts/quickstart.sh — completed steps are skipped."
  exit 2
else
  printf '%s\n' "$OUT" | tail -5 >&2
  fail "copilot live probe did not return the skill-body facts."
fi

say ""
say "QUICKSTART COMPLETE: both tools installed, materialized, and live-verified from $ROOT"
say "Launch from this directory:  claude   |   copilot"
