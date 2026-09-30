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
- This workspace ships **no `CLAUDE.md`** (dropped 2026-09-30, ledger C4):
  native `AGENTS.md` load is the only path, guarded by
  `scripts/check-agents-md-load.sh` (version floor 2.1.277, live marker
  probe, and a hard fail if a `CLAUDE.md` ever reappears without the
  `@AGENTS.md` bridge — an annex-only file silently suppresses the
  native read).
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

## `--bare` — know what it strips **[PROVEN]**

- `--bare` loads only built-in agents (`claude`, Explore, general-purpose,
  Plan, statusline-setup): project `.claude/agents/` and project skills are
  NOT loaded. Right tool for cheap auth probes and minimal-context
  questions; wrong tool for project work. (E6 pilot, 2026-09-30.)
- It is a flag, not a mode with a product name — don't present it as one.

## Telemetry **[PROVEN live 2026-09-30]**

- `OTEL_LOG_RAW_API_BODIES=file:<dir>` writes the untruncated Messages API
  request/response JSON plus an `index.jsonl` linker — the ground truth
  for "what did the harness actually send" (system prompt, tool schemas,
  cache fields).
- Telemetry and content capture can only be enabled from shell env, user,
  or managed settings — a repo's `.claude/settings.json` cannot turn them
  on. Config is read at startup; relaunch after changing it.

## Hooks

- Failures fire `PostToolUseFailure`, not `PostToolUse` (which is
  success-only). Routing failures to `PostToolUse` captures nothing —
  our adapter's first bug, caught by E4.

## Headless runs honor write approvals

- In `-p` mode the agent stops and asks before writing files where an
  approval boundary applies instead of writing silently. Automation that
  expects files must either run where approval is granted or treat
  "awaiting approval" as a first-class outcome. (E6 pilot.)
