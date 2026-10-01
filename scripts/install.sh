#!/usr/bin/env bash
# One-install entry point: canonical/ -> both tools' native layouts.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/adapters.py
echo "Install complete. Next step: ./scripts/quickstart.sh --structural-only"
echo "(structural verification: 8/8 skills, 12/12 agents, 5+5 MCP servers per tool). Then launch claude or copilot from this directory."
