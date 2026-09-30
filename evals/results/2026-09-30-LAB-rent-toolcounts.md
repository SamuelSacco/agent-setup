# LAB — description rent + per-agent tool counts, re-measured

Date: 2026-09-30 (W2 triage stream, branch `lab/triage`). Method: parse
frontmatter of `canonical/agents/*.md` and `canonical/skills/*.md` at
phase-2 head 3556e46; tokenize with tiktoken `cl100k_base`. No API spend.
Claude's tokenizer differs from cl100k by a few percent on English prose;
no counting variant tried comes close to rescuing the packet figures.

## X2 — description rent (packet: "~300 tokens roster v2 vs ~546 V1 12")

Per-agent description tokens (description-only / name+description):

| agent | desc | name+desc |
|---|---|---|
| backend | 23 | 25 |
| build-error-resolver | 42 | 47 |
| code-architect | 31 | 35 |
| code-explorer | 24 | 28 |
| code-reviewer | 34 | 38 |
| data-scientist | 29 | 34 |
| doc-updater | 48 | 52 |
| planner | 35 | 38 |
| refactor-cleaner | 46 | 51 |
| security-reviewer | 49 | 53 |
| tdd-guide | 38 | 42 |
| ux-ui | 23 | 26 |
| **all 12** | **422** | **469** |

Full-frontmatter variant (name+description+model_hint+tools_hint): 739.

- Packet's ~546 for the V1 12: **not reproduced** — 422 / 469 / 739 under
  the three methods. Closest is name+desc at −14%.
- Packet's ~300 for the roster-v2 six: the six names do not map 1:1 to
  files. explorer→code-explorer (24), code-reviewer (34),
  build-error-resolver (42), security-reviewer (49), evaluator→
  data-scientist (29) = **178** for five; **task-runner has no canonical
  file**. Even granting task-runner the maximum observed rent (49), the
  six total 227 < ~300 under every method.
- Direction survives: six ≈ 0.42–0.48× the twelve. The rule "fewer
  defaults ≈ half the listing rent" is consistent with the files; the
  point figures are not.
- Omitted surface: 8 skill descriptions = **430 tokens**. Total listing
  rent actually carried (12 agents + 8 skills, descriptions only) = 852.
  Any rent budget that counts agents only understates by ~half.
- Packet's "~3.5k for all-68 ECC": implies 51.5 tokens/agent vs our
  ports' 35.2 average. Plausible (ECC originals are longer; ports were
  adapted) but the ECC source is not in this repo — UNVERIFIABLE here.

**Verdict: packet figures REFUTED as measurements; qualitative rule
stands.** No derivation file for the original figures exists in the repo.

## X1a — loaded tools per agent (talk heuristic: "≤ ~35 tools per agent")

- Canonical agents declare `tools_hint` only: 2–4 abstract categories
  (read / edit / shell / search) per agent.
- Emitted configs carry **no** restriction: `grep '^tools:'` over
  `.claude/agents/*.md` and `.github/agents/*.md` = 0 files. The adapter
  projects name+description into both tools; hints never become a
  `tools:` allowlist.
- Therefore every agent loads the full session toolset. Measured session
  tool counts (OTEL decomposition, `evals/results/2026-09-30-otel-
  instrumentation.md`, ledger S8–S10): Claude default = **12 tool defs**;
  Copilot default = **23 tools** (incl. 5 from an auto-connected MCP
  server).
- 12 and 23 are both < 35: the heuristic is satisfied vacuously, by the
  harnesses' defaults, not by anything this setup does. No artifact in
  the repo ties 35 (or any threshold) to a task outcome.

**Verdict: "per-agent tool budgeting is implemented in this setup"
REFUTED. The 35 threshold itself remains UNVERIFIABLE folklore.**
