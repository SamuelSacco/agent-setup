#!/bin/bash
# usage: pv-skills.sh <claude|copilot> <skillA> <skillB>
# One run, two skills invoked by name; evidence = Skill tool_use (claude stream-json)
# or skill.invoked events (copilot json) + SKILLS-OK reply.
TOOL="$1"; A="$2"; B="$3"
PV=/home/hatch/workspace/p2/portverify
mkdir -p "$PV/logs"
prompt="Invoke the '${A}' skill now (load it with your skill mechanism). When its content loads, do not carry out its workflow; just note it as loaded. Then invoke the '${B}' skill the same way. After both skills have loaded, reply with exactly: SKILLS-OK ${A} ${B}"
if [ "$TOOL" = claude ]; then
  "$PV/pv-claude.sh" "$prompt" --output-format stream-json --verbose --max-turns 8 \
    > "$PV/logs/claude-skills-${A}+${B}.jsonl" 2>/dev/null
else
  "$PV/pv-copilot.sh" "$prompt" \
    > "$PV/logs/copilot-skills-${A}+${B}.json" 2>"$PV/logs/copilot-skills-${A}+${B}.err"
fi
echo "$TOOL skills $A + $B done"
