#!/bin/bash
# usage: pv-claude.sh <prompt> [extra claude args...]  (cwd fixed to case proj, isolated HOME)
CASE=${PV_CASE:-/home/hatch/workspace/p2/portverify/case}
PROMPT="$1"; shift
cd "$CASE/proj" || exit 1
HOME="$CASE/home" /home/hatch/workspace/tools/bin/claude -p "$PROMPT" \
  --model claude-haiku-4-5-20251001 \
  --permission-mode acceptEdits \
  --allowedTools 'Write Edit Bash Read Glob Grep Skill Task' "$@"
