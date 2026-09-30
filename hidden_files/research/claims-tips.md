# Claims verification: /advisor and rubber duck

Researched 2026-09-30. Read-only web research; primary sources only for verdicts.

---

## Claim 1: Claude Code `/advisor` pairs Sonnet with Opus to save tokens

**Verdict: PROVEN** (with one correction to the "saves tokens" framing — see below).

### What it actually is

`/advisor` is a real, documented Claude Code command (also available as the
`advisorModel` setting and the `--advisor` launch flag). It attaches a second,
stronger model as an "advisor" to your session. Your main model (the executor)
does all the work; at decision points — before committing to an approach, when
stuck on a recurring error, before declaring done — Claude decides to consult the
advisor, which reads the full conversation transcript server-side and returns
short strategic guidance (typically 400–700 text tokens). The executor then
continues. It is labeled experimental in-product ("Advisor Tool (experimental)").

Primary source: https://code.claude.com/docs/en/advisor

### Sonnet 5.5 / Opus 5.5, named specifically

Both model names appear explicitly in Anthropic's pairing rules:

- Claude Code docs pairing table: main model **"Sonnet 5.5 or Sonnet 5"** accepts
  advisors "Fable, Opus 4.7 or later, Sonnet 5 or later" — i.e. Opus 5.5 is a
  valid advisor for a Sonnet 5.5 session. You can pass the full model ID, e.g.
  `/advisor claude-opus-5-5`.
- API model-compatibility table lists **Claude Sonnet 5.5 → Claude Opus 5.5** as
  a valid executor/advisor pair.

Primary source: https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool
(pairing table also at https://code.claude.com/docs/en/advisor)

Pairing rule: the advisor must be at least as capable as the main model. The
direction matters — Opus 5.5 as *main* with a Sonnet advisor is **rejected** by
both Claude Code and the API.

### The token story, honestly

This is where the popular framing oversells it:

- Advisor calls are **not free and not token-neutral**. Each consult is billed at
  the **advisor model's rates, in addition to** your main model's usage
  (API billing: advisor tokens are separate `advisor_message` iterations;
  subscription plans: counts toward plan limits).
- Each call makes Opus read the **entire transcript fresh** — by default there is
  no caching of the advisor's own read between calls ("Each advisor call
  processes the full transcript anew, with no reuse between calls"). Advisor
  output runs ~1,400–1,800 tokens per call including thinking.
- The savings are **relative, not absolute**: you save versus running Opus as
  your main model for the whole session, because the bulk of generation happens
  at Sonnet rates and Opus is only paid for short guidance bursts. Anthropic's
  own version of the claim: "You get close to advisor-solo quality while the
  bulk of token generation happens at executor-model rates," and "pairing a
  Sonnet executor at medium effort with an Opus advisor achieves intelligence
  comparable to Sonnet at default effort, at lower cost."
- On short or simple tasks the advisor is **pure overhead** — Anthropic says so
  directly ("It adds less value on short tasks where there is little to plan").
  Claude Code doesn't cap how often Claude consults; you steer it in your
  prompt ("consult the advisor before you continue").

So: "Sonnet does the work, Opus sanity-checks at decision points, cheaper than
Opus-everything" = accurate. "Saves tokens" unqualified = misleading.

Practical requirements: Anthropic API only (not Bedrock / Google / Foundry);
Claude Code must be able to fetch feature flags (e.g. `DISABLE_TELEMETRY` turns
it off); disable entirely with `CLAUDE_CODE_DISABLE_ADVISOR_TOOL=1`.

---

## Claim 2: GitHub Copilot CLI "comes with a rubber duck"

**Verdict: PROVEN.**

### What it actually is

Copilot CLI ships with a built-in **rubber duck agent**: an independent critic
that reviews the main agent's plans, code, and tests and returns structured,
severity-categorized feedback (Blocking / Non-blocking / Suggestions). It's
named after rubber-duck debugging, but unlike a real duck it talks back.

The signature design choice: the duck deliberately runs on a **different model
family** from the one driving your session — Claude driving → GPT critic, or
vice versa — so the critic doesn't share the driver's blind spots. The critic
model is picked automatically per invocation based on your current session model.

Primary source: https://docs.github.com/en/copilot/concepts/agents/copilot-cli/rubber-duck

Key facts from GitHub's docs:

- Built into Copilot CLI; available with all Copilot plans (org must have the
  CLI policy enabled).
- Consulted **automatically** at high-leverage moments: after planning a
  non-trivial change, mid-implementation, after writing tests, and reactively
  after repeated failures. Skipped for small, well-understood changes.
- Invoke it explicitly three ways: natural language ("Rubber duck your plan"),
  the slash command `/rubber-duck <prompt>`, or start a session as one with
  `copilot --agent rubber-duck` (the latter two per GitHub's own
  copilot-dev-days workshop repo and the Copilot CLI command reference at
  https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference).
- Read-only: it can explore the codebase but cannot edit files or run
  state-changing commands. The main agent decides what to do with the critique.
- It summarizes its critique in the timeline rather than dumping it verbatim.
- Cost note from GitHub: consulting it "adds some latency and involves
  additional model usage" — the bet is that catching issues early saves more
  than the consult costs.

One availability nuance from launch coverage: it initially rolled out behind
the CLI's experimental flag; GitHub's current docs describe it as a standard
built-in agent, so treat "experimental" references as launch-era, not current.

---

## Summary for the tips & tricks section

| Claim | Verdict | One-line truth |
|---|---|---|
| Claude Code `/advisor` pairs Sonnet with Opus | PROVEN | Sonnet drives, Opus advises at decision points; Sonnet 5.5 + Opus 5.5 is a documented valid pairing. Cheaper than Opus-only, but each consult costs extra Opus-rate tokens — not a free lunch. |
| Copilot CLI has a rubber duck | PROVEN | Built-in cross-model critic agent (Claude↔GPT). Auto-consulted on non-trivial work; `/rubber-duck` or "rubber duck your plan" to invoke manually. |

### Primary sources

1. Claude Code advisor docs — https://code.claude.com/docs/en/advisor
2. Claude API advisor tool docs (pairing table, cost/billing) — https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool
3. GitHub Docs, "About the rubber duck agent" — https://docs.github.com/en/copilot/concepts/agents/copilot-cli/rubber-duck
4. GitHub Docs, Copilot CLI command reference (`/rubber-duck`) — https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference
