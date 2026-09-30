#!/usr/bin/env bash
# One-install entry point: canonical/ -> both tools' native layouts.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/adapters.py
echo "Install complete. Launch claude or copilot from this directory."
