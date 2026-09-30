# E4 backup — Claude session summary of the 5 induced failures

Cost: $0.0257 · turns: 6

Command (5): **Exit code 2** — explicit exit

**Summary:**
1. `python --version` → **127**
2. `cat ./no-such-file-xyz.txt` → **1**
3. `python3 -m unittest demo.does_not_exist` → **1**
4. `python3 -m json.tool ./demo/bad.json` → **1**
5. `exit 2` → **2**
