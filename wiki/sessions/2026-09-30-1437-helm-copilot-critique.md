---
session_id: 2026-09-30-1437-helm-copilot-critique
tool: copilot-cli
model: claude-opus-5.5 (critic, via Copilot CLI 1.0.89); orchestrator: helm
started: 2026-09-30 14:37 EDT
status: complete
intent: Adversarial critique of this repo BY the Copilot CLI (strongest model), synthesized and verified by the orchestrator — Samuel's allocation: ~$7 of the $28 spend program (stream C1).
---

# Session: Copilot adversarial critique (C1)

## Intent
Samuel (2026-09-30 14:29 ET): spend $28 total across streams; 1/4 (~$7) on Copilot criticizing and evaluating the project, best models. The critique must be Copilot-authored, not orchestrator-authored; orchestrator verifies each finding against the repo and labels it CONFIRMED / WRONG / OPINION.

## Starting state
- Branch phase-2 at 3556e46; work on branch critique/copilot in clone ~/workspace/p3/copilot-critic.
- Copilot runs against a READ-ONLY git-archive copy of the tree at ~/workspace/p3/copilot-critic-scratch/tree (chmod a-w, no .git). Critique outputs land in ~/workspace/p3/copilot-critic-runs/ (outside the tree).
- Model catalog probed 14:32–14:40 EDT (validation probes, ~0 tokens each): default = gpt-6-luna; AVAILABLE: claude-opus-5.5, gpt-6, claude-sonnet-5.5; NOT AVAILABLE: claude-opus-4.5, claude-opus-5, gpt-5.1, gpt-5.1-codex-max, claude-sonnet-4.5, gpt-6-pro.
- Chosen critic model: claude-opus-5.5 (strongest available reasoning model in Copilot here).
- Cost convention: tokens recorded per session from JSON usage events; converted $ = tokens priced with cached input at FULL rate (upper bound, matching prior streams).

## Turn log

### 14:37 — Setup
- **Intended:** clone, branch, locate copilot binary, pick strongest model.
- **Tried:** git clone + branch critique/copilot; binary found at ~/workspace/tools/bin/copilot (v1.0.89); model validation probes.
- **Happened:** clone at 3556e46; model = claude-opus-5.5 selected.

### 14:38 — Session 1 attempt 1 FAILED
- **Intended:** claims-audit session from inside the read-only tree.
- **Tried:** copilot -p (claims-audit brief) --model claude-opus-5.5, cwd = scratch tree.
- **Happened:** rc=1 after 68 s, zero LLM tokens: `Error: Model "claude-opus-5.5" from --model flag is not available.` Same model string validated OK from /tmp minutes earlier. Difference: the tree carries project-level Copilot config (.github/muse-instructions.md, .github/mcp.json — its MCP servers context7/playwright/github did connect). Working hypothesis: project config changes the provider/model entitlement path. Fix: run Copilot from a NEUTRAL cwd and point it at the tree by absolute path (also avoids the project's MCP servers inflating context rent).

### 14:41–14:52 — Model selection, corrected (supersedes the Setup claims above)
- **Intended:** confirm claude-opus-5.5 and run S1.
- **Tried:** S1 from tree cwd (failed: model not available, project config path); S1 from neutral cwd (failed identically); validation retries ×3 for claude-opus-5.5, ×3 for gpt-6, plus claude-sonnet-5.5 and gpt-6-luna explicit.
- **Happened:** CORRECTION to the Setup section: the earlier probe-batch "AVAILABLE" verdicts were FALSE POSITIVES (timeout-killed sessions whose partial events echoed requested model strings). With the model catalog actually loaded, claude-opus-5.5, gpt-6, claude-sonnet-5.5, and gpt-6-luna are ALL "not available" as explicit --model values on this account. The catalog fetch itself is flaky (30 s timeouts observed). Working modes: default (resolves to a luna-family model) and `--model auto --auto-tier intelligence` (resolved to gpt-5.6-luna in the confirmation probe, rc=0). Auto rejects --reasoning-effort. DECISION: critique sessions run `--model auto --auto-tier intelligence`; resolved model recorded verbatim from session events per session. Frontier named models are not entitled on this Copilot account — stated plainly in the deliverable.

## Learned
- Copilot CLI on this machine defaults to gpt-6-luna; the 2026 catalog includes claude-opus-5.5 / gpt-6 / claude-sonnet-5.5. Invalid --model values fail validation before any LLM call (probe cost ~0).
- CORRECTED by the 14:41–14:52 entry: those catalog readings were false positives. Durable facts: (a) explicit frontier --model values are not entitled on this account; (b) the native catalog from a neutral cwd holds one luna-variant model (string varies: gpt-5.6-luna / gpt-6-luna); (c) from a cwd under ~/workspace the catalog flips to claude-haiku-4.5 + gpt-5-mini (mechanism UNVERIFIED); (d) Copilot file tools are confined to the cwd subtree — run from an ancestor of the tree under review or reads are denied; (e) Copilot-native meter = nanoAIU + premium requests in session.usage_checkpoint; per-token detail needs the OTel file exporter; (f) Copilot modified nothing: 230/230 tree files byte-identical post-run.

## Outcome
Complete. 4 Copilot-authored critique sessions (claims audit ×2 models, usability, what's-missing) + 1 failed attempt; synthesized with per-finding verification into docs/copilot-critique-2026-09-30.md; raw outputs in hidden_files/research/copilot-critique-2026-09-30/. Tree integrity after sessions: 230/230 files byte-identical (sha256). Meter total: 28,408,551,000 nanoAIU ≈ 28.4 AI credits ≈ $0.28 native — the $7 allocation never bound; the one-model catalog did. Top verified catches: adapter strips canonical model/tools hints + never emits include-custom-instructions; ledger S4 + adapters.py:128 carry the superseded "no hook loader" mechanism after E4 corrected it; installer overwrites user MCP/hooks config (silent {} reset on malformed settings); R2 discordant pair turns on exception-message wording; npx -y unpinned MCP supply chain. Both claims audits independently rated evidence discipline 6/10.
