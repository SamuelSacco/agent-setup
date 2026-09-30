#!/bin/bash
# usage: pv-copilot.sh <prompt> [extra copilot args...]  (cwd fixed to case proj, isolated HOME)
CASE=${PV_CASE:-/home/hatch/workspace/p2/portverify/case}
PROMPT="$1"; shift
cd "$CASE/proj" || exit 1
export COPILOT_PROVIDER_TYPE=anthropic COPILOT_PROVIDER_BASE_URL=https://api.anthropic.com \
       COPILOT_PROVIDER_MODEL_ID=claude-haiku-4-5-20251001 COPILOT_ALLOW_ALL=true
COPILOT_PROVIDER_API_KEY="$(python3 /home/hatch/workspace/skills/anthropic/bin/claude_api_key_helper.py)"
export COPILOT_PROVIDER_API_KEY
HOME="$CASE/home" timeout ${PV_TIMEOUT:-600} /home/hatch/workspace/tools/bin/copilot -p "$PROMPT" --output-format json "$@"
