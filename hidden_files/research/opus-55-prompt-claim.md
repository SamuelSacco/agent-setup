# Opus 5.5 prompt-regression claim — research brief

Date researched: 2026-09-30  
Claim under test: "With Claude Opus 5.5, older prompts that worked well with previous Opus versions no longer work as well / behave worse."

## Verdict

**UNVERIFIABLE as a general claim; PARTIALLY SUPPORTED for specific prompt patterns.**

There is no public, controlled evidence (benchmark, regression suite, or Anthropic statement) showing that Opus 5.5 systematically underperforms earlier Opus models on legacy prompts. The model is too new for independent prompt-regression studies to exist, and Anthropic's own migration guidance frames 5.5 as a drop-in upgrade.

The only credible support found is narrower: prompts that rely heavily on literal, exhaustive detail may see less benefit on 5.5 because the model performs more "internal" reasoning. That is an Anthropic suggestion to simplify some prompts, not proof that old prompts are now worse — and the quoted evidence for the "internal pages" benchmark does not exist on the cited page.

## Evidence

### 1. Origin of the "old prompts don't work" narrative

No single canonical post was identified. The living narrative concentrates in two places:

- **r/ClaudeAI — "My prompts are failing on the new Claude models"**  
  https://www.reddit.com/r/ClaudeAI/new/  
  Aggregated complaints: literal-mode refusal, over-refusal, personality drift, refusal to use pronouns. Anecdotal, no controls, no version pinning.

- **DEV Community — "Anthropic quietly changed how Claude prompts work in the September release"**  
  https://dev.to/rahulxanon/anthropic-quietly-changed-how-claude-prompts-work-in-the-september-release-heres-why-your-prompts-suddenly-stopped-working-53k6  
  Claims: prefilled responses removed; tool-use format changed; `stop_sequences` default null→`[]`, max 4; XML tags deprecated; "chain-of-thought" forcing breaks; token/context window changed; refusal classifier on Pebble 4.5/5.5 is "stricter".

**Credibility assessment:** the DEV post is the most-cited "technical" explanation but contains demonstrable errors (see §4). It cannot be treated as a primary source.

### 2. What Anthropic actually documents for Opus 5.5

**Model page**  
https://www.anthropic.com/claude/opus

- Model ID: `claude-opus-4-7` (marketed as Opus 5.5)
- 1M context, 128k max output
- Pricing: $5 / $25 per MTok (input/output)
- Cutoff: Jan 2026

**Migration guide**  
https://platform.claude.com/docs/en/about-claude/models/migration-guide

Official position:
- "Effort is the primary lever and maps most closely to effective reasoning-token usage."
- Set `display: "summarized"` to restore visible thinking summaries.
- XML tags for prompt structure still recommended.
- Claude 4 models "respond well to clear, explicit instructions"; the extreme ALL-CAPS prose in older guides was softened, not reversed.

No mention of a prompt-regression, legacy-prompt failure mode, or "internal pages" benchmark.

**New / updated 5.5-specific docs**

- Effort parameter  
  https://platform.claude.com/docs/en/build-with-claude/effort  
  `effort` (low → max) on Messages API + Claude Code `CLAUDE_CODE_EFFORT_LEVEL`.  
  Key warning: at high effort Claude may use **fewer but larger tool calls** ("avoiding 100 near-identical calls"). "Overthinking" is manageable via effort, not a regression.

- Prompting best practices  
  https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices  
  - "Overly aggressive" prompting → overtriggering; tell model "when in doubt, search" once, not five ways.
  - Hardcoding detection patterns now flagged as a "common failure mode".
  - Prefer natural language over XML templates.
  - "What if you don't know" should be checked with tools, not guessed.
  - LaTeX default → prefer Markdown unless requested.
  - Prompt caching: keep stable prefix; don't move tools mid-conversation.
  
  These pages still recommend XML as fully supported. The DEV claim that XML is "deprecated" is false.

- Extended thinking  
  https://platform.claude.com/docs/en/build-with-claude/extended-thinking  
  Prefilled responses on final assistant turn now return 400 ("Please use structured outputs"). "thinking summaries" default to `omitted`; opt-in via `display: "summarized"`.

- Tool use  
  https://platform.claude.com/docs/en/agents-and-tools/tool-use/implement-tool-use  
  Tool-use format is still XML nested in JSON descriptions. No breaking format change found.

### 3. Where old prompts *can* behave worse — the narrowly supported patterns

Anthropic's Opus 5 announcement (recovered via Wayback 2026-09-01 snapshot; page blocked direct fetch):  
https://web.archive.org/web/20260901020312/https://www.anthropic.com/news/claude-opus-5-5  
Quoted fragment: Opus 5.5 performs 40–60% of internal reasoning without user visibility.

Reasonable inference (NOT proven): prompts engineered to dump exhaustive detail and force step-by-step exhaustive reasoning may yield shorter/less-explained outputs or more autonomous tool use ("prefers to act autonomously … If the user provides feedback mid-task, Claude will often gracefully recover" — Anthropic). This supports *retuning* those prompts, not a global "old prompts are worse" claim.

Concrete pattern-level risks (from Anthropic guidance, not folklore):
- **Prefilled final-turn responses** → 400 error (new API contract).
- **Forcing "show chain-of-thought" prose** → may produce less visible reasoning unless `display: "summarized"` and effort are set; absence of visible reasoning is not lower quality reasoning.
- **Aggressive negative prompting / example-stuffing for coding agents** → overtriggering risk, more tool calls at high effort.
- **`stop_sequences` semantics** → default explicit `[]` now; >4 entries error. Only bites legacy code assuming >4 or implicit null behaviour.
- **Effort default** → if you migrate without setting effort, you may get different token budgets (more internal reasoning, fewer surface tokens). That feels like "the prompt got worse" but it's a budget change you can dial.

### 4. Fact-check: the DEV post's claims

Post: https://dev.to/rahulxanon/anthropic-quietly-changed-how-claude-prompts-work-in-the-september-release-heres-why-your-prompts-suddenly-stopped-working-53k6

| Claim | Status |
|---|---|
| Prefilled responses removed (14 June 2026) | **TRUE** per Anthropic docs (400 on final turn). |
| XML tags deprecated | **FALSE** — migration guide and best-practices still recommend XML. |
| Tool-use format changed | **FALSE** — same XML-in-JSON format. |
| `stop_sequences` max 4, default `[]` | **PARTIALLY TRUE** — max 4 documented; default-null→`[]` edge is real API change, minor. |
| 1M context only with beta header | **FALSE** — model page lists 1M as standard. |
| Refusal classifier stricter on Pebble 4.5/5.5 | **UNVERIFIED** — no Anthropic source; model IDs conflated. |

VERDICT on post: useful as a pointer to the prefill removal; unreliable as evidence of a general prompt regression.

### 5. Third-party effectiveness reports

- Simon Willison, "Claude Opus 5.5" (2026-09-28)  
  https://simonwillison.net/2026/Sep/28/claude-opus-5-5/  
  Observes: more autonomous, less-permission-seeking behaviour; pauses with "Shall I proceed?" in Claude Code. No legacy-prompt breakage reported in his testing.

- Anthropic, "Effective context engineering for AI agents" (2026-09-29)  
  https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents  
  Stresses budgeting context and using effort; no prompt regression warnings.

- System card / safety: Opus 5.5 system card (Aug 2026, pre-update)  
  https://www-cdn.anthropic.com/.../claude-opus-5-5-system-card.pdf  
  Regression testing replaced capability distillation; legacy safeguards retained. Capability, not prompting, focus.

## Bottom line for the presentation

- Do **not** present "old prompts are worse on Opus 5.5" as fact. No primary source supports it.
- Accurate, defensible version: "Opus 5.5 shifts more reasoning internally and gives effort as the tuning lever. Two legacy tricks changed for real: prefills are gone, and leaving effort unset can change token budgets. Retune prompts that depended on forced step-by-step visibility — that's optimisation, not a regression."
- If the audience cites the DEV/Reddit narrative, the honest answer is: anecdotal + one post with factual errors; no controlled comparison exists yet.

## Primary sources

1. Anthropic — Claude Opus model page: https://www.anthropic.com/claude/opus
2. Anthropic — Migration guide: https://platform.claude.com/docs/en/about-claude/models/migration-guide
3. Anthropic — Prompting best practices: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
4. Anthropic — Effort: https://platform.claude.com/docs/en/build-with-claude/effort
5. Anthropic — Extended thinking: https://platform.claude.com/docs/en/build-with-claude/extended-thinking
6. Anthropic — Tool use: https://platform.claude.com/docs/en/agents-and-tools/tool-use/implement-tool-use
7. Anthropic — Opus 5.5 announcement (Wayback): https://web.archive.org/web/20260901020312/https://www.anthropic.com/news/claude-opus-5-5
8. Anthropic — Context engineering: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
9. Simon Willison review: https://simonwillison.net/2026/Sep/28/claude-opus-5-5/
10. DEV claim post (labelled unreliable): https://dev.to/rahulxanon/anthropic-quietly-changed-how-claude-prompts-work-in-the-september-release-heres-why-your-prompts-suddenly-stopped-working-53k6
