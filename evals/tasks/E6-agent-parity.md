# E6 — Shared-agent parity

**Claim S6:** The same canonical specialist agent produces equivalent-quality 
work in both tools.

**Pre-registered threshold:** PASS if blind-scored outputs differ by ≤ 1 
rubric point (of 10) on 3 matched tasks, per agent.

## Steps
1. Pick `backend`, `ux-ui`, `data-scientist` from `canonical/agents/`.
2. Give each agent the same bounded task in Claude Code and in Copilot CLI 
   (fresh checkout per run).
3. Score outputs blind (scorer doesn't know which tool produced which): 
   correctness, convention fit, test presence, clarity.

## What this catches
Format drift — e.g. one tool ignoring the agent body, truncating it, or 
applying different tool permissions. Any of those is an adapter fix, and the 
fix is re-tested here.
