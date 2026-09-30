# Tips & Tricks — Claude Code

Researched 2026-09-30 against Anthropic's docs. Verdicts in 
`docs/claims-ledger.md`; every claim here is labeled.

## `/advisor` — Sonnet drives, Opus advises **[PROVEN]**

- `/advisor` (also `advisorModel` setting, `--advisor` flag) attaches a stronger 
  model as advisor. Your main model does the work; at decision points it consults 
  the advisor, which reads the full transcript and returns short guidance.
- Documented pairing: **Sonnet 5.5 → Opus 5.5** is valid (`/advisor claude-opus-5-5`). 
  The reverse (Opus main, Sonnet advisor) is rejected.
- **Cost truth:** cheaper than running Opus as main, but NOT free. Each consult is 
  billed at advisor rates on top of your session, and each call re-reads the whole 
  transcript. On short tasks it's pure overhead — Anthropic says so.
- Requirements: Anthropic API (not Bedrock/Vertex/Foundry); telemetry off 
  (`DISABLE_TELEMETRY`) disables it; `CLAUDE_CODE_DISABLE_ADVISOR_TOOL=1` kills it.

## Instruction files **[PROVEN]**

- Since v2.1.277 (2026-09-18), Claude Code reads `AGENTS.md` natively — **only** 
  when no `CLAUDE.md`/`CLAUDE.local.md` exists in the cwd or above it.
- Robust bridge: make `CLAUDE.md`'s first line `@AGENTS.md` (this workspace does). 
  Never double-loads; hooks fire; works everywhere.
- Verify with `/context` — the file should appear under **Memory files**.
- `/doctor prompt-audit` (v2.1.283+) audits CLAUDE.md/AGENTS.md/rules/skills for 
  stale or conflicting instructions. Run it after big instruction edits.
- `.claude/rules/` with `paths:` frontmatter = rules that load only for matching 
  files. Use for scoped conventions instead of bloating the root file.
- Output styles are a separate layer (response voice/format), not a CLAUDE.md 
  replacement. Gotcha: a custom style drops built-in coding instructions unless 
  `keep-coding-instructions: true`.

## Prompting on Opus 5.5 **[PARTIALLY SUPPORTED patterns]**

- "Old prompts broke on Opus 5.5" as a blanket claim: **UNVERIFIABLE** — see the 
  claim note [[opus-55-prompt-regression]].
- Real changes: prefilled final-turn responses now error; `effort` is the tuning 
  lever (unset effort = changed token budget); forced exhaustive visible 
  step-by-step may show less surface reasoning. Retune, don't panic.
- XML structure is still recommended by Anthropic. Ignore posts claiming otherwise.
