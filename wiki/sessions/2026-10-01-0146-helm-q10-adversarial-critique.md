---
session_id: 2026-10-01-0146-helm-q10-adversarial-critique
tool: claude-code
model: coordinator (Helm subagent)
started: 2026-10-01 01:46 ET
status: complete
intent: Q10 — two independent external critics (fresh Claude Opus, Copilot CLI BYOK) attack public master 2abc02b; triage every finding, apply FIX-NOW and LEDGER-CORRECTION items in-branch.
---

# Session: Q10 adversarial critique of public master

## Intent
External-reader adversarial review of the shipped tree: which claims an outside expert would dispute, what is overstated, what is missing, what breaks for a stranger. Deliverable branch lab/q10-adversarial-critique: both critiques verbatim under evals/results/, triage doc docs/q10-triage-2026-10-01.md, fixes applied in-branch.

## Starting state
- Master 2abc02b (public). Cumulative fleet metered spend ~$12.19 of $150 ceiling; Q10 wave cap $6.
- Critics are blind to each other and to overnight internals; both get only the public tree + claims ledger + an identical attack charter.
- Triage clone: ~/workspace/q10-triage on branch lab/q10-adversarial-critique.

## Turn log

### 01:46 — Wave setup
- **Intended:** Spawn both critics in parallel; create triage branch.
- **Tried:** Worker A: fresh Claude (claude --bare, apiKeyHelper, claude-opus-5-5) in ~/workspace/q10-critic-claude. Worker B: Copilot CLI 1.0.90 BYOK Anthropic in ~/workspace/q10-critic-copilot. Identical charter, five fronts: claims, overstatement, missing, stranger test, consistency.
- **Happened:** Both workers spawned; triage clone created at 2abc02b.

### ~01:56 — Copilot critic completed
- 26 findings, one run, 7m 59s, model claude-opus-5-5 over BYOK. Tokens (stderr footer): 2.2M in (2.1M cached, 141.5K written), 16.8K out → $2.284 converted (upper bound). Critique at evals/results/2026-10-01-Q10-critique-copilot.md (verbatim copy on this branch).
- Headline finding [critical]: 3 canonical frontmatter blocks are invalid YAML (unquoted `: ` in descriptions; adapters fm_block emitted unquoted) — Copilot CLI logged parse errors and exposed only 7/9 skills, 11/12 agents in a live session. Coordinator verified on disk (PyYAML) before triage: exactly those 3 files fail.

### ~02:02 — Claude critic FAILED, API credit exhausted
- Primary run (claude --bare + apiKeyHelper): "Not logged in", $0. Fallback (no --bare) ran ~13.5 min (76,062 output tokens, 10,514,990 cache-read, 2 subagents) and terminated api_error: **"Credit balance is too low"**, total_cost_usd **$5.39878** (exact envelope), zero findings. Its results file (header + the error verbatim) ships on this branch as the honest record.
- Coordinator probe after the fact: fresh minimal `claude -p` returns "Credit balance is too low" at $0 — the Anthropic API credit balance is exhausted; every API-key-metered run (Claude arms, Copilot BYOK) fails until topped up.
- Wave spend: $5.39878 + $2.284 = **≈ $7.68 vs the $6 cap — breached**, entirely by the failed run's burn.

### ~02:05–02:35 — Triage + fixes (docs/q10-triage-2026-10-01.md)
- All 26 Copilot findings classified: FIX-NOW 14, LEDGER-CORRECTION 7, DISPUTE 2 (+ disputed components in 3 more), DEFER 3 (+ deferred components in 4 more). Every fix below is on this branch.
- Code: fm_block emits double-quoted scalars + round-trip abort; parse_frontmatter unquotes; 3 canonical descriptions quoted at source; empty-string MCP env values dropped at emission (github token can no longer be overridden by an emitted ""); install prints the S4 failure-capture warning and the unset-GitHub-token note; install.sh derives counts from canonical/ (9/9, 12/12, 5+5) and points at the HOME-write disclosure; quickstart --structural-only skips CLI install/network entirely, §3 parses all 42 emitted frontmatters (PyYAML, quote-contract fallback), checks ~/.copilot/mcp-config.json as the Copilot scope, and the Node WARN now states all 5 MCP servers are npx-based.
- Docs: README parity wording scoped; setup.md §4 discloses every write incl. ~/.copilot/mcp-config.json (machine-wide effect, last-install-wins, no uninstaller), §2 gains a Copilot login verify step, troubleshooting names the user-scope file, §6 counts runtime-derived; AGENTS.md §8 Copilot SessionEnd wording corrected (trigger PROVEN under trust); deck.html 7 stale strings corrected (S6 scope, MCP emission, E3 row + status, E5 −38% at both sites, self-review merged note).
- Ledger: PARTIAL defined in the key + self-audit disclosure in the header; amendments/corrections on S1, S3 (discard attribution + row folded to 4 cells), S6 (claim scoped), S12 (combined rule no longer called pre-registered; S3 cross-ref updated), S14 (Q10 correction: discovery broken for 3 capabilities at 2abc02b; fix + owed live re-verification), S15 (claim scoped), S19 (retracted mechanism replaced), S21 (verdict split; stale enforcement sentence replaced), S23 (separator), S24 (evidence cell); S25 scope note; table reordered, blank-line breaks removed — 31 S-rows × 4 cells verified.

## Learned
- Emitting YAML by string interpolation (`f"{k}: {v}"`) is a silent capability-killer: a `: ` inside a description invalidates the whole frontmatter block, strict parsers drop the capability, and a count-based verifier certifies the breakage. Emitters must quote and round-trip-validate; verifiers must parse, not count.
- A pre-registered bar met exactly is not evidence of a flaw in the test; post-hoc combination rules are — and the ledger's own words must not call them pre-registered anywhere, including the verdict cell.
- Metered critic runs need a hard spend circuit-breaker inside the run, not just a worker instruction: the Claude fallback burned $5.40 with no findings because nothing stopped it before the balance did.

## Outcome
Complete. Branch lab/q10-adversarial-critique: both critique files verbatim (Claude file = the failure record), triage doc with all 26 findings classified, FIX-NOW + LEDGER-CORRECTION applied, install.sh exit 0, structural verify PASS incl. bare-environment run, negative parse test recorded. Owed when API credit is restored: Claude critic re-run, live Copilot discovery re-verification, live probe redesign (finding 7).
