#!/usr/bin/env bash
# One-install entry point: canonical/ -> both tools' native layouts.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/adapters.py
# Counts are derived from canonical/ at runtime — a hardcoded count here
# went stale the day a ninth skill landed (Q10 finding 3, 2026-10-01).
skills=$(ls canonical/skills/*.md | wc -l | tr -d ' ')
agents=$(ls canonical/agents/*.md | wc -l | tr -d ' ')
mcp=$(ls canonical/mcp/*.json | wc -l | tr -d ' ')
echo "Install complete. Next step: ./scripts/quickstart.sh --structural-only"
echo "(structural verification: $skills/$skills skills, $agents/$agents agents, $mcp+$mcp MCP servers per tool). Then launch claude or copilot from this directory."
echo "Note: install also writes the Copilot user-scope MCP config ~/.copilot/mcp-config.json (merged, never replaced) — see docs/setup.md section 4."
