# Phase 2 external signal sweep — 2026-09-30

Scope: external check of the claims in `docs/phase2-packet-2026-09-30.md` ahead of the 16:00 ET presentation. Every factual item carries a source URL and a date (publication/release date where visible, otherwise "accessed 2026-09-30"). Sections: provider documentation (primary), third-party measurement, practitioner opinion. Provenance is labeled where a claim rests on search-result text rather than a directly opened page.

## Verdict summary

- No packet finding is refuted outright. Four claims need qualification before they go on stage (items 1–4 below).
- Biggest Q&A risk: two independent studies find context files do **not** generally improve coding-agent correctness. The orientation claim must stay narrow (codebase, model, protocol).
- ToxicSkills numbers: verified exactly against the primary source.
- Prompt-audit story: verified, but only in its narrow form. Blanket "old prompts degrade new models" is distorted; Anthropic's own current docs say adjacent-generation prompts carry over.
- Both CLIs moved in the last 30 days in ways that touch packet claims (Claude Code 2.1.277/2.1.283; Copilot CLI 1.0.86/1.0.89).

## Required wording changes before 16:00

1. **Orientation.** Say: "NetworkX, Haiku 4.5, our orientation protocol: 8/8 vs base 6/8 across two four-task batches." Do not say: "Orientation files improve coding-agent success." Reason: ETH Zurich (revised 2026-09-29) and Khatri (2026-07-28) both find no general correctness gain from context files. Sources below.
2. **CLAUDE.md suppression.** Qualify: "In the default project-instructions mode we tested, an annex-only CLAUDE.md prevented AGENTS.md from loading." Anthropic's current docs confirm this as the **default** behavior and themselves recommend the `@AGENTS.md` bridge the packet keeps. Support exists only from Claude Code v2.1.277; user-level and managed CLAUDE.md files do **not** trigger suppression.
3. **Copilot `postToolUseFailure`.** Do not say "never fires." GitHub documents the event and processes its output. Safe form: "GitHub documents `postToolUseFailure` and processes its output; in our tested CLI setup it did not fire for shell exit failures, so shell failure capture parses `postToolUse` payloads." The universal claim rests on Phase 2 live testing only; no confirming GitHub issue was found (searched 2026-09-30).
4. **Copilot custom agents and repo instructions.** As of Copilot CLI v1.0.86 (2026-09-17), repository instruction files (`AGENTS.md`, `copilot-instructions.md`, `CLAUDE.md`) are **opt-in** for custom agents via `include-custom-instructions: true` in frontmatter. Any claim that custom agents automatically receive repo orientation must be version- and definition-qualified.
5. **ToxicSkills.** Use exact figures: 3,984 skills; 36.82% with at least one security flaw; 13.4% critical; 76 confirmed malicious. Do not shorten 36.82% to "malicious" — only 76 were confirmed malicious. Source: Snyk, study data as of 2026-02-05, https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/ (accessed 2026-09-30).

## 1. Provider documentation (primary)

### Claude Code — AGENTS.md support and CLAUDE.md precedence

- Anthropic's memory docs state the default ("Project instructions" = `claude-md-or-agents-md`): with no `CLAUDE.md`/`CLAUDE.local.md` in the working directory or above, Claude reads `AGENTS.md`; if a CLAUDE file exists there, Claude reads the CLAUDE files **only**. A `CLAUDE.md`, `.claude/CLAUDE.md`, or `CLAUDE.local.md` in the working directory or any parent triggers this; `~/.claude/CLAUDE.md`, managed CLAUDE.md, and `.claude/rules/` files do not. Anthropic explicitly recommends an `@AGENTS.md` import inside CLAUDE.md for sharing one file, and says keeping the import never double-loads AGENTS.md. Docs: https://code.claude.com/docs/en/memory (accessed 2026-09-30). **Packet Finding 4: VERIFIED for the default configuration.**
- Configuration values exist beyond the default: `claude-md-and-agents-md` (both), `claude-md` (CLAUDE only), `managed-only`. The setting is ignored in project/local settings files. Same docs URL, accessed 2026-09-30.
- Version floor: AGENTS.md support requires Claude Code **v2.1.277**; before v2.1.281, some sessions (Amazon Bedrock, telemetry disabled) read CLAUDE.md only, and in those sessions the `@AGENTS.md` import is the delivery path. Same docs URL, accessed 2026-09-30.
- Changelog entry for v2.1.277, dated 2026-09-18: "Added AGENTS.md support: in a project with no CLAUDE.md, Claude Code reads AGENTS.md instead" (not yet on Bedrock/Vertex/Foundry at release). Official changelog: https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md (entry text verified via changelog mirrors, accessed 2026-09-30).
- Packet tested Claude Code 2.1.285. Third-party release tracking dates 2.1.285 to 2026-09-29 and no newer stable was found in searches on 2026-09-30. Sources: https://www.havoptic.com (release index, accessed 2026-09-30); Arch AUR `claude-code 2.1.285-1`, updated 2026-09-29 (accessed 2026-09-30). Label: latest found, not absolute.
- Docs also state: CLAUDE.md files are context, not enforced configuration; Anthropic targets under 200 lines per file; contradictory instructions may be picked arbitrarily. https://code.claude.com/docs/en/memory (accessed 2026-09-30).

### Copilot CLI — hooks

- GitHub's hooks reference documents `postToolUseFailure`: fires after a tool completes with a failure; output is processed and can supply recovery guidance via `additionalContext`. The reference states all documented events are supported by the CLI. https://docs.github.com/en/copilot/reference/hooks-reference (accessed 2026-09-30).
- Same reference: `sessionEnd` fires on session termination with `reason` in {complete, error, abort, timeout, user_exit}, and its **output is NOT processed** — a sessionEnd hook can run cleanup commands but cannot inject context or block. On `/clear`, sessionEnd fires detached with `reason: "user_exit"`. Same URL, accessed 2026-09-30.
- Consequence for the packet's cleanup claim: automatic session-end cleanup in Copilot is a "runs commands" mechanism only. Keep the packet's boundary — skill invocation PROVEN, automatic cleanup/forget routine UNPROVEN end-to-end.

### Copilot CLI — agents, skills, MCP precedence (now documented)

- GitHub's CLI plugin reference gives an explicit first-loaded order, verified in the page itself. Built-ins (agents: explore, task, code-review, general-purpose, research) are always present and cannot be overridden. Custom agents, first loaded wins (dedup by ID): `~/.copilot/agents/` → project `.github/agents/` → parent `.github/agents/` → project `.claude/agents/` → parent `.claude/agents/` → `--add-dir` → plugin agents (install order) → remote org/enterprise. Skills, first loaded wins (dedup by name): project `.github/skills/` → `.agents/skills/` → `.claude/skills/` → parent equivalents → `~/.copilot/skills/` → `~/.agents/skills/` → plugin skills → `COPILOT_SKILLS_DIRS`. MCP servers are the exception: **last loaded wins** (dedup by name), user `~/.copilot/mcp-config.json` lowest, `--additional-mcp-config` highest. https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference (accessed 2026-09-30).
- Packet implication: "no reliable precedence exists" is now stale for the plugin surface. Keep the no-duplicate-names rule — first-loaded-wins means a duplicate silently shadows — but do not claim precedence is undocumented.
- Skill locations corroborated independently: project skills in `.github/skills/`, `.agents/skills/`, `.claude/skills/`; personal in `~/.copilot/skills/`, `~/.agents/skills/`; each skill is a directory with `SKILL.md` (required frontmatter: `name`, `description`). https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills (accessed via search result, 2026-09-30). **Packet claim "Copilot reads `.agents/skills/` natively": VERIFIED.**

### Copilot CLI — releases in the last 30 days

- **v1.0.86, 2026-09-17** (release page opened 2026-09-30): custom agents opt into repository instruction files via `include-custom-instructions: true`. https://github.com/github/copilot-cli/releases/tag/v1.0.86
- **v1.0.85, 2026-09-16** (search result, 2026-09-30): added dedicated `copilot plugin|mcp|skill enable/disable`; the older `copilot plugins enable/disable --plugin|--mcp|--skill` form was replaced. Check any slide/handout showing the old form. https://github.com/github/copilot-cli/releases/tag/v1.0.85
- **v1.0.88, changelog entry dated 2026-09-22** (search result, 2026-09-30): custom-agent `reasoning-effort` now applies on selection; hook commands without explicit `cwd` run in project root again; MCP recovery fixes. https://github.com/github/copilot-cli/blob/main/changelog.md
- **v1.0.89, 2026-09-28** (GitHub release via search result, 2026-09-30): Copilot now reads Claude Code rule files in `.claude/rules` as custom instructions; adds `claude-opus-5.5` support. Latest Copilot CLI found. https://github.com/github/copilot-cli/releases/tag/v1.0.89

### Vercel Labs `skills` CLI (`npx skills`)

- Current README (opened 2026-09-30): install methods are symlink (recommended — "symlinks from each agent to a canonical copy; single source of truth") or copy (`--copy`, independent copies). Per-agent project paths: GitHub Copilot → `.agents/skills/`; Claude Code → `.claude/skills/`. Command surface is skills-only (`add`, `use`, `list`, `find`, `remove`, `update`, `init`) — no agents/hooks/MCP/plugin acquisition. https://github.com/vercel-labs/skills (repository created 2026-01-14; 47 releases; accessed 2026-09-30).
- **Packet Finding 3: VERIFIED** against the primary README, including the Claude-only copy-mode drift risk (`--copy` writes directly into the agent path). No deprecations or command removals found in current docs (accessed 2026-09-30). Not checked: individual release notes from the last 30 days.

## 2. Third-party measurement

### Context files and task success — the contradiction to prepare for

- Gloaguen et al. (ETH Zurich / LogicStar), "Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?", arXiv 2602.11988, submitted 2026-02-12, **last revised 2026-09-29**: "providing context files does not generally improve task success rates, while increasing inference cost by over 20% on average" — held across LLMs, agents, LLM-generated and developer-committed files. Context files remain useful for specifying non-standard practices. https://arxiv.org/abs/2602.11988 (accessed 2026-09-30).
- Khatri, "Do Context Files Help Coding Agents? A Two-Agent Ablation Study on Real Repositories", arXiv 2607.27250, submitted 2026-07-28: 17 real tasks, 3 repositories, 288 evaluated runs across Claude Code and Codex; "context strategy does not measurably move correctness on either agent" (equivalence bound ≤10–15pp); agents fail on implementation skill, not missing repository knowledge. https://arxiv.org/abs/2607.27250 (accessed 2026-09-30).
- Read: two independent null results vs. the packet's positive NetworkX result (n=8, one codebase, one model, one protocol). The packet result is not refuted; the generalization is. This is the most likely expert Q&A challenge.

### Specialist agents and multi-agent systems

- Anthropic (provider, but measurement-bearing), "How we built our multi-agent research system", 2025-06-13: multi-agent (Opus 4 lead, Sonnet 4 subagents) beat single-agent Opus 4 by **90.2%** on an internal **research** eval; agents use ~4× chat tokens, multi-agent systems ~15×; token usage alone explains ~80% of BrowseComp performance variance. Anthropic's own scoping caution: domains requiring shared context or many inter-agent dependencies are a poor fit, and **most coding tasks** involve fewer truly parallelizable tasks than research. https://www.anthropic.com/engineering/multi-agent-research-system (accessed 2026-09-30; figures now verified in the primary page).
- Cognition, "Don't Build Multi-Agents", 2025-06-12 (as quoted in a third-party research note, accessed 2026-09-30): share full context and traces; conflicting implicit decisions across agents produce bad results. https://cognition.com/blog/dont-build-multi-agents
- Net corroboration for the packet: subagents pay when work is separable and context-isolated (research); that does not validate domain-persona rosters for coding. Consistent with the packet's specialist result (same 3/4, +55% turns, +8.5% cost, zero added solves) and with the roster kill-test (an agent must differ in tools, model, context isolation, permissions, or output contract).

### Context overhead

- Hong, Troynikov & Huber (Chroma), "Context Rot: How Increasing Input Tokens Impacts LLM Performance", July 2025: across **18 LLMs**, performance degrades non-uniformly as input length grows even on controlled tasks of constant difficulty; a single distractor measurably lowers accuracy and multiple distractors compound it. https://research.trychroma.com/context-rot (accessed 2026-09-30; verified in the primary page).
- Supports the packet's "context rent" framing and the ≤~35-tools heuristic as a budget rule. It does **not** prove a universal 35-tool cutoff; keep 35 labeled as a heuristic.

### Skills supply chain (Snyk ToxicSkills)

- Snyk, study data as of 2026-02-05: 3,984 skills scanned (ClawHub + skills.sh); 1,467 (36.82%) with at least one security flaw; 534 (13.4%) with at least one critical issue; 76 human-confirmed malicious payloads, 100% with malicious code patterns and 91% also using prompt injection; no code signing, no security review, no sandbox by default on ClawHub. https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/ (accessed 2026-09-30). **Packet numbers: VERIFIED exactly.**
- Provenance label: Snyk is a security vendor and the study author — third-party measurement relative to this project, not a neutral academic benchmark.

## 3. Practitioner opinion (label as opinion; not benchmarks)

- "Instruction files get ignored" is a recurring complaint genre. A third-party aggregation (2026-07-11) reports 19 distinct r/ClaudeAI threads matching "CLAUDE.md ignores" in one search, with users attributing it to context-limit deprioritization. https://github.com/directiveforge/directiveforge/blob/HEAD/research/2026-07-11-user-pain-raw/2c-reddit.md (accessed 2026-09-30). Consistent with Anthropic's own docs framing (context, not enforcement) and with the packet's verify-from-disk rule.
- AGENTS.md "split brain" complaint, August 2026: a Reddit digest (2026-08-27) reports a high-engagement post (r/AgentsOfAI, 664 points) on Shopify CEO Tobi Lutke arguing Claude Code should read `AGENTS.md` because CLAUDE.md-only support creates split-brain in multi-tool repos. https://github.com/vibewatch/vibewatch.github.io/blob/HEAD/docs/reddit/ai-agent/2026-08-27.md (accessed 2026-09-30). Stage relevance: Claude Code 2.1.277 (2026-09-18) post-dates the complaint — a clean "the surface moved" example.
- Subagent cost autopsy, single practitioner, self-measured (dev.to, accessed 2026-09-30): subagents were 48% of one month's Claude Code bill while their returned output was 0.9% of tokens; each subagent started at ~51K tokens of fixed context (system prompt, tool schemas, CLAUDE.md, memory) re-sent per request; fixes were cap agents per run, batch small units, trim starting context, hand off before ~400K tokens. https://dev.to/ji_ai/claude-code-subagents-were-48-of-my-bill-their-output-was-09-e4i — n=1 self-report; corroborates the mechanism (agents × requests × context size), not a rate.
- CLAUDE.md staleness warning (Medium, 2026-08-15): instruction files "turn into stale documentation that the model follows with confidence; treat it like code: keep it small, review changes." https://medium.com/@sebuzdugan/claude-md-helps-but-everyone-is-ignoring-how-fast-it-turns-into-stale-documentation-that-the-model-ca6ade4b6eb0 (accessed 2026-09-30).
- Copilot CLI practitioner guidance converges with the packet (third-party guide files, accessed 2026-09-30): instructions for always-on guidance, a skill for an on-demand workflow, a custom agent for context isolation/restricted tools, and **hooks when a behavior must always happen, because instructions only guide the model**. https://github.com/arisng/github-copilot-fc/blob/HEAD/skills/copilot-cli-agent-customization/SKILL.md
- Retrieval caveat: direct `site:reddit.com` searches for r/ClaudeAI, r/GithubCopilot, r/ChatGPTCoding returned no results on 2026-09-30; the sentiment above rests on secondary aggregations and practitioner posts, not directly retrieved Reddit threads. Do not present it as Reddit-primary evidence.

## 4. Prompt-audit guidance: verified / distorted / not found

### Verified

- Anthropic blog, "Reducing cost and improving performance with Claude Platform", originally published **2026-09-08**, updated after the Opus 5.5 launch (2026-09-22): prompts accumulate instructions that patch old model weaknesses; named anti-patterns are verification rituals ("verify twice"), thoroughness/emphasis boosters ("be maximally thorough", "CRITICAL: YOU MUST ALWAYS…"), mandatory procedures and scratchpad scaffolds, stale few-shot examples, contradictory rules, and dated configuration (e.g. manual thinking budgets). Fix offered: the `claude-api` skill's **`/claude-api prompt-audit`**, which per the blog covers anything in the working directory including CLAUDE.md and skills. https://claude.com/blog/reducing-cost-and-improving-performance-with-claude-platform (accessed 2026-09-30).
- Updated Opus 5.5 numbers on the current page: on Anthropic's customer-support benchmark with six planted legacy prompts, Opus 4.8 → Opus 5.5 migration alone cut cost ~**18%** (cheaper Opus 5.5 input/cache pricing); one prompt-audit pass cut a further ~**9%**; accuracy rose ~**2 percentage points**. Mechanisms: a retired thinking setting made the API reject requests outright; contradictory refund rules made Opus 5.5 withhold four owed refunds; a manual scratchpad collided with built-in thinking so tool calls were written inside reasoning and never executed. Same URL, accessed 2026-09-30.
- Lead author: Lance Martin (mirror metadata for the 2026-09-08 post, accessed 2026-09-30: https://github.com/qiankuang8/blog/blob/HEAD/sources/orig/reducing-cost-and-improving-performance-with-claude-platform.md). The ClaudeDevs rollout post is dated 2026-09-08: https://x.com/ClaudeDevs/status/2097369738968195513 (secondary-recorded, accessed 2026-09-30).
- Adjacent-generation carry-over, Anthropic's own docs: "Existing Claude Opus 5 prompts should perform well without changes" — Prompting Claude Opus 5.5, https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5 (accessed 2026-09-30). "It performs well out of the box on existing Claude Sonnet 4.6 prompts" — Prompting Claude Sonnet 5, https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5 (accessed 2026-09-30; verified in the primary page). The same docs flag the real migration risks as **settings**, not prompt text: effort levels do not map 1:1 across models, and manual `thinking: {type: "enabled", budget_tokens}` is removed on Sonnet 5 (400 error).
- A second Claude Code surface exists and is distinct: **`/doctor prompt-audit`** (alias `/checkup prompt-audit`), added in Claude Code **v2.1.283, released 2026-09-25**, "to audit your CLAUDE.md files, skills, agents and commands for prompting patterns written for older models". Official changelog: https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md (entry quoted in search results, accessed 2026-09-30). Do not conflate the two commands on stage.
- Mansel Scheffel video exists and is on-topic: "Anthropic Just Told Us How to Prompt Opus 5.5 (copy this)", https://www.youtube.com/watch?v=kMXh9YDCKCI (page opened 2026-09-30; chapter list tracks the Opus 5.5 prompting guide: effort calibration, removing "think step by step", unattended runs, rechecking). Publication date not visible in the fetched page; search metadata points to approximately 2026-09-24.

### Distorted

- "Old prompts degrade new models" as a blanket claim. Supported form: **specific legacy scaffolding and carried-over settings** (verification rituals, emphasis boosters, forced scratchpads, stale few-shots, contradictory rules, manual thinking budgets) can cost tokens and accuracy on frontier models. Anthropic's docs simultaneously say Opus 5 → 5.5 and Sonnet 4.6 → 5 prompts carry over fine. Sources: blog and docs URLs above, accessed 2026-09-30.
- Quoting 18% / +9% / +2pts as expected savings. Those figures come from Anthropic's own benchmark with deliberately planted anti-patterns and a price-driven migration component; they are an upper-bound illustration, not a workload forecast. Source: https://claude.com/blog/reducing-cost-and-improving-performance-with-claude-platform (accessed 2026-09-30).
- Conflating versions of the numbers: the original 2026-09-08 Opus 5 version reported prompt-audit at **14.6%** additional cost reduction and **+5.3%** accuracy (mirror of the original article, accessed 2026-09-30: https://github.com/byteflare-co/anthropic-engineering-ja/blob/HEAD/articles/claude_en/135_reducing-cost-and-improving-performance-with-claude-platform.md). The 18% / 9% / 2pts figures are the later Opus 5.5 re-run.
- "Anthropic published 12 new rules for Opus 5.5." Refuted: the "12 rules" framing is video packaging; Anthropic's guide has eleven symptom-organized sections and does not use the word "rules". Third-party analysis: https://pub.towardsai.net/anthropics-opus-5-5-prompting-guide-has-11-sections-and-more-of-them-say-delete-than-add-b241dcc1500e (accessed via search result, 2026-09-30).
- Third-party claim (The Prompt Shelf, accessed 2026-09-30) that `/claude-api prompt-audit` only activates in repos importing the Anthropic SDK conflicts with the blog's broader "anything in the working directory" scope. Treat the SDK-activation caveat as reported, not settled: https://thepromptshelf.dev/blog/claude-code-doctor-prompt-audit-vs-claude-api-2026/

### Not found

- Exact text of a Lance Martin X post promoting `/claude-api prompt-audit` at the Opus 5.5 launch: a post exists at https://x.com/RLanceMartin/status/2102575471502528989, cited as a source in Opus 5.5 launch coverage (Podtail/Podbean "AI with Kyle" episode pages, accessed 2026-09-30: https://podtail.com/podcast/ai-with-kyle/), and its status ID timestamp resolves to 2026-09-23 01:47 UTC (2026-09-22 ET, launch day). The post text itself was not directly verified (direct fetch blocked 2026-09-30). Lance Martin's authorship and promotion of the guidance in the 2026-09-08 rollout is verified (above); the launch-day X post is **partially verified — URL and date yes, text no**.
- No independent (non-Anthropic) replication of the prompt-audit savings figures was found (searched 2026-09-30). The numbers are vendor-reported from a single planted-anti-pattern benchmark.
- No evidence that prompt-audit guidance applies to Copilot CLI configuration; all sources above are Anthropic surfaces.

## 5. Other not-found / negative results (searched 2026-09-30)

- No GitHub issue confirming a Copilot CLI shell-exit gap for `postToolUseFailure`. The packet's claim stands on Phase 2 live testing alone; label it that way.
- No `npx skills` deprecations or command removals in current Vercel Labs documentation (accessed 2026-09-30).
- No Claude Code stable newer than 2.1.285 found.

## Source index

Provider documentation (primary):
- https://code.claude.com/docs/en/memory — accessed 2026-09-30
- https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md — v2.1.277 (2026-09-18), v2.1.283 (2026-09-25)
- https://docs.github.com/en/copilot/reference/hooks-reference — accessed 2026-09-30
- https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference — accessed 2026-09-30
- https://github.com/github/copilot-cli/releases/tag/v1.0.86 — 2026-09-17
- https://github.com/github/copilot-cli/releases/tag/v1.0.89 — 2026-09-28
- https://github.com/vercel-labs/skills — accessed 2026-09-30
- https://claude.com/blog/reducing-cost-and-improving-performance-with-claude-platform — published 2026-09-08, updated post-2026-09-22
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5 — accessed 2026-09-30
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5 — accessed 2026-09-30

Third-party measurement:
- https://arxiv.org/abs/2602.11988 — submitted 2026-02-12, revised 2026-09-29
- https://arxiv.org/abs/2607.27250 — submitted 2026-07-28
- https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/ — data as of 2026-02-05
- https://research.trychroma.com/context-rot — July 2025
- https://www.anthropic.com/engineering/multi-agent-research-system — 2025-06-13 (provider-published measurement)

Practitioner opinion:
- https://dev.to/ji_ai/claude-code-subagents-were-48-of-my-bill-their-output-was-09-e4i — accessed 2026-09-30
- https://www.youtube.com/watch?v=kMXh9YDCKCI — approximately 2026-09-24
- https://sparkone.nl/en/blog/claude-code-prompt-audit/ — 2026-09-27 (practitioner walkthrough of the two prompt-audit commands; corroborates the /doctor vs /claude-api split)
