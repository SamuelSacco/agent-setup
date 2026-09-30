#!/bin/bash
# usage: pv-agents.sh <claude|copilot> <agent...>
# Per agent: --agent <name> session; task = read probe-input.txt, write marker file, reply AGENT-OK.
TOOL="$1"; shift
PV=/home/hatch/workspace/p2/portverify
mkdir -p "$PV/logs"
for name in "$@"; do
  marker="${PV_CASE:-$PV/case}/proj/probe-out/${TOOL}-agent-${name}.txt"
  rm -f "$marker"
  prompt="Read probe-input.txt. Then write a file probe-out/${TOOL}-agent-${name}.txt whose entire contents are: ${name} followed by a space and the probe token from probe-input.txt. Then reply with exactly: AGENT-OK ${name}"
  if [ "$TOOL" = claude ]; then
    "$PV/pv-claude.sh" "$prompt" --output-format json --agent "$name" --max-turns 6 \
      > "$PV/logs/claude-agent-${name}.json" 2>/dev/null
    cost=$(python3 -c "import json;d=json.load(open('$PV/logs/claude-agent-${name}.json'));print(d.get('total_cost_usd'))" 2>/dev/null || echo PARSE_FAIL)
    echo "claude agent $name cost=$cost"
  else
    "$PV/pv-copilot.sh" "$prompt" --agent "$name" \
      > "$PV/logs/copilot-agent-${name}.json" 2>"$PV/logs/copilot-agent-${name}.err"
    echo "copilot agent $name done rc=$?"
  fi
  if [ -f "$marker" ]; then echo "  MARKER: $(cat "$marker")"; else echo "  MARKER: MISSING"; fi
done
