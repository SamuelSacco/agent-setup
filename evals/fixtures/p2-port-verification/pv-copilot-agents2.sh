#!/bin/bash
# usage: pv-copilot-agents2.sh <agentA> [agentB]   (honors PV_CASE / PV_TIMEOUT)
# One Copilot session, task-tool delegation(s); evidence = marker files.
A="$1"; B="${2:-}"
PV=/home/hatch/workspace/p2/portverify
if [ -z "$B" ]; then
  prompt="Use your task tool to delegate to the '${A}' agent: the agent must read probe-input.txt and write a file probe-out/copilot-agent-${A}.txt whose entire contents are: ${A} followed by a space and the probe token from probe-input.txt. When the delegation is complete, reply with exactly: AGENT-OK ${A}"
  tag="${A}"
else
  prompt="Use your task tool to delegate to the '${A}' agent: the agent must read probe-input.txt and write a file probe-out/copilot-agent-${A}.txt whose entire contents are: ${A} followed by a space and the probe token from probe-input.txt. Then use your task tool to delegate to the '${B}' agent: the agent must read probe-input.txt and write a file probe-out/copilot-agent-${B}.txt whose entire contents are: ${B} followed by a space and the probe token from probe-input.txt. When both delegations are complete, reply with exactly: AGENTS-OK ${A} ${B}"
  tag="${A}+${B}"
fi
"$PV/pv-copilot.sh" "$prompt" > "$PV/logs/copilot-agents-${tag}.json" 2>"$PV/logs/copilot-agents-${tag}.err"
echo "copilot agents $tag rc=$?"
for n in $A $B; do
  f="${PV_CASE:-$PV/case}/proj/probe-out/copilot-agent-${n}.txt"
  if [ -f "$f" ]; then echo "  MARKER $n: $(cat "$f")"; else echo "  MARKER $n: MISSING"; fi
done
