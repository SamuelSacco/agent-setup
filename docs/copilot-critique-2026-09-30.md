# Copilot adversarial critique — 2026-09-30

Method: the critique was authored by the GitHub Copilot CLI (v1.0.89), not by the
orchestrator. Copilot ran in allow-all mode against a read-only copy of this tree
(git archive of phase-2 @ 3556e46; tree integrity re-verified after all sessions:
230/230 files byte-identical). The orchestrator then verified each finding against
the repo and labeled it CONFIRMED / WRONG / OPINION. Copilot's say-so is not
evidence; the counter-reference is given wherever a finding fails.

Raw outputs (critique texts, session JSONL, OTel traces):
`hidden_files/research/copilot-critique-2026-09-30/`

## Model reality (read before citing this critique)

- Explicit frontier models are NOT entitled on this Copilot account.
  `claude-opus-5.5`, `gpt-6`, `claude-sonnet-5.5`, `gpt-6-luna` all fail with
  "not available" once the model catalog actually loads (several retries each).
- The native catalog visible from a neutral directory contains exactly one
  model: a GPT luna variant. Session logs record it verbatim as `gpt-6-luna`
  (3 sessions); one probe resolved `gpt-5.6-luna`. The string varies by run.
- From a working directory under `~/workspace`, the catalog flips to
  `claude-haiku-4.5` + `gpt-5-mini` (mechanism UNVERIFIED — a workspace-anchored
  provider/plugin configuration is the suspected cause). One claims-audit
  session ran there before this was understood; it is kept, labeled by model.
- Sessions run: 4 critique sessions (claims audit ×2 models, usability,
  what's-missing) + 1 failed attempt (workspace-confinement denied all reads;
  no critique produced). All critique sessions used `--model auto
  --auto-tier intelligence`; auto rejects `--reasoning-effort`.

## Spend vs the $7 allocation

Copilot-native meter (from `session.usage_checkpoint` in each session log):

| Session | Model | nanoAIU | Premium req | Tokens (OTel, luna sessions) |
|---|---|---|---|---|
| S1 claims (failed, access denied) | gpt-5.6-luna | 857,601,500 | 1 | — |
| S1 claims | claude-haiku-4.5 | 21,938,490,000 | 0.33 | not captured (no OTel) |
| S1 claims | gpt-6-luna | 2,245,847,000 | 1 | in 1,162,000 · out 29,784 · cache-read 500,972 · cache-write 79,998 |
| S2 usability | gpt-6-luna | 1,811,470,000 | 1 | in 847,052 · out 25,572 · cache-read 358,420 · cache-write 65,076 |
| S3 what's missing | gpt-6-luna | 1,555,142,500 | 1 | in 645,212 · out 21,616 · cache-read 262,415 · cache-write 60,167 |
| Probes (~10 tiny validation runs) | luna variants | not metered individually | ~0 | negligible |

Total: 28,408,551,000 nanoAIU ≈ 28.4 AI credits ≈ **$0.28** at GitHub's
$0.01/AI-credit rate (conversion convention: 1 AI credit = 1e9 nanoAIU).
Under this project's prior token-conversion convention (cached input priced at
full rate, GPT-5-class $5/M in · $30/M out), the three luna sessions' tokens
convert to ≈ $22 — an upper bound that does not reflect Copilot-native billing.
Either way the binding constraints were the one-model catalog and session
count, not dollars. The $7 allocation was not the limit.

## Findings, by severity (orchestrator-verified)

### High

1. **The adapter strips canonical agent intent, and Copilot agents lose the
   shared instructions.** `scripts/adapters.py` `install_agents()` emits only
   `name` + `description` for BOTH tools; canonical `model_hint`/`tools_hint`
   are dropped (the source file admits it: `canonical/agents/code-reviewer.md`
   frontmatter carries `model_hint: strong-reasoning`,
   `tools_hint: [read, shell, search]`, and its provenance comment says
   "adapter strips both"). The adapter also never emits
   `include-custom-instructions: true` (zero hits in `scripts/`, `canonical/`),
   which the packet itself documents as required for Copilot custom agents to
   receive repo instructions. Generated Copilot agents therefore run without
   the AGENTS.md workflow the setup claims is shared. — **CONFIRMED** (S2)
2. **Ledger S4 rationale is stale and wrong.** `docs/claims-ledger.md` S4:
   "Copilot: REFUTED on installed CLI v1.0.89 — binary contains no hook
   loader; 0/5." The cited evidence file corrects this in its own addendum:
   `evals/results/2026-09-30-E4.md:56` — later evidence "contradicted the
   'no hook loader' attribution… repo hooks exist" (trust-gated; the real gap
   is `postToolUseFailure` not discriminating shell exits). The ledger never
   absorbed the correction. The same superseded sentence lives in
   `scripts/adapters.py:128`. The PARTIAL verdict is defensible; the stated
   mechanism is refuted by the project's own file. — **CONFIRMED** (S1-luna)
3. **Runtime supply chain is `npx -y` unpinned.** All five
   `canonical/mcp/*.json` servers run `npx -y` with unversioned or `@latest`
   package specs (e.g. `@modelcontextprotocol/server-filesystem`,
   `@modelcontextprotocol/server-github`, context7 `@latest`); `adapters.py`
   copies them into both tools' configs with no lockfile, digest, allowlist,
   or provenance check. The repo's own narrative headlines third-party skill
   supply-chain risk (ToxicSkills) while its runtime path is trust-latest.
   — **CONFIRMED** (S3)
4. **The installer destroys existing user configuration.** `install_mcp()`
   rewrites root `.mcp.json` and `.github/mcp.json` wholesale (no merge);
   `install_hooks()` replaces the entire `hooks` object in
   `.claude/settings.json` (`settings["hooks"] = settings_hooks`), and on
   malformed settings JSON the `JSONDecodeError` handler
   (`scripts/adapters.py:149`) silently resets it to `{}` before writing.
   No backup, dry-run, warning, or rollback; `docs/setup.md` tells users to
   re-run the installer after every canonical edit. — **CONFIRMED** (S2, S3)
5. **One of the two discordant pairs under the PROVEN orientation headline
   turns on assertion text.** `evals/results/2026-09-30-P2-realcode-ab.md:
   193-197`: on R2 the base arm raised the correct exception
   (`NetworkXPointlessConcept`) with message "No nodes in graph"; the real
   fix's test matches `null graph`, so the pair is discordant on message
   wording, not behavior. This is disclosed in the results file; it appears
   in neither the packet headline nor the addendum's pooled "11/12 vs 9/12."
   Effective positive evidence for S12 is two pairs, one wording-dependent.
   — **CONFIRMED** (S1-luna)
6. **S14's blanket PROVEN vs per-surface verdicts.** The ledger's S14
   ("19 ports discoverable and invocable in BOTH tools", PROVEN) sits over a
   port report that records Playwright PARTIAL as shipped (root-sandbox
   failure; passes only with `--no-sandbox` in a scratch config; non-root
   use UNVERIFIABLE) and authenticated GitHub operations untested. The
   bundle label should be PARTIAL or stay per-surface. — **CONFIRMED** as a
   calibration defect (S1-luna)
7. **Orientation generalizability is pooled away in the headline.** Rich
   (3/4 vs 3/4, zero discordant pairs, UNVERIFIABLE) contributes no positive
   signal; both critics independently flagged the addendum's pooled
   "11/12 vs 9/12 across two codebases" framing. The packet's scoped stage
   wording is the defensible claim. — **CONFIRMED** (S1 both models; agrees
   with this project's own addendum caveat — Copilot adds emphasis, not a
   new fact)
8. **S16's ceiling problem is not foregrounded in the packet.** 2/8 pairs
   completed, both concordant passes on tasks Copilot base already solves;
   an orientation win was structurally impossible on the completed set.
   Verdict UNVERIFIABLE is correct; the constraint is visible in the
   addendum, not where the claim is introduced. — **CONFIRMED** (S1-haiku;
   agrees with ledger S16 — emphasis, not new fact)

### Medium

9. **Evidence custody.** Raw run artifacts for the headline evals live under
    `~/workspace/p2/…`, and the addendum's verification-stack reports
    (refutation, docs fact-check, prompt audit) live in `~/workspace/…` —
    outside the repo. "Disk-derived" describes the method; a reviewer cannot
    re-derive the headlines from the tree alone. — **CONFIRMED** (both S1s)
10. **Ledger S2 drops the tested direction.** E2 tested Copilot→Claude only
    (`evals/results/2026-09-30-E2.md:10-14`: Tool A = Copilot, Tool B =
    Claude). Ledger S2 reads "a session in tool A is continuable by tool B,"
    direction-free. Reverse direction untested. — **CONFIRMED** (S1-luna)
11. **S8's "past the 60KB cap" is not demonstrated by its cited run.** The
    ledger asserts bodies "size-complete past the 60KB cap"; the cited
    instrumentation file's only measured request body is 5,417 B, and the
    size-complete statement there is labeled a docs fact-check caveat, not a
    measurement (`evals/results/2026-09-30-otel-instrumentation.md:17-22`).
    The claim may be true; the cited evidence does not show it.
    — **CONFIRMED** (S1-luna)
12. **C1/C2 are PROVEN on research notes.** Ledger C1/C2 cite
    `research: hidden_files/research/claims-tips.md`, not a run — against
    this repo's own standard ("PROVEN (we ran it)", AGENTS.md §5). C4 is at
    least labeled "PROVEN (docs)" and cites live canary probes for part.
    — **CONFIRMED** (S1-luna)
13. **The quickstart is partly fictional.** README step 1 is `cd agent-setup`
    — no clone command anywhere in the README. README's tree depicts
    `canonical/plugins/` and an `adapters/` directory; neither exists
    (`canonical/` = agents, hooks, mcp, skills; generation is
    `scripts/adapters.py` writing in place). `docs/setup.md:3` promises
    "from zero… in ~15 minutes," but its §1 "Install the tools" runs only
    `claude --version` / `copilot --version` — no install instructions, no
    version-floor or OS matrix anywhere. — **CONFIRMED** (S2, S3)
14. **`docs/toolchain.md` points at files that do not exist.**
    `toolchain.md:12,13,17` route setup through
    `canonical/skills/gitlab.md`, `canonical/mcp/coralogix.json`,
    `canonical/mcp/atlassian.json`. None are in the tree. Actionable-looking
    guidance that cannot be followed as written. — **CONFIRMED** (S3)
15. **Setup "done" criteria contradict the shipped ledger.** `docs/setup.md:
    59`: setup is only "done" when E1/E2 "flip to PROVEN" — the shipped
    ledger already marks S1/S2 PROVEN, E4 is PARTIAL, and setup.md gives no
    commands for running any of the three probes. A stranger cannot tell a
    broken install from an unsupported feature. — **CONFIRMED** (S2)
16. **GitHub MCP ships an empty token with no documented route.**
    `canonical/mcp/github.json` sets `GITHUB_PERSONAL_ACCESS_TOKEN: ""`;
    its description says "Set the env token before use," but no doc explains
    a secret-safe way to inject it without hand-editing generated config
    that AGENTS.md forbids editing. — **CONFIRMED** (S2)
17. **The eval runner is not an isolation boundary.** `scripts/run_eval.py`
    runs agents as the invoking user with host network and ambient
    credentials: Copilot arm sets `COPILOT_ALLOW_ALL="true"` (~line 175),
    Claude arm allows `Write Edit Bash …` (~lines 143-144). Fresh-tree +
    disk grading is reproducibility, not containment; no doc states a
    trusted-task requirement. — **CONFIRMED** (S3)
18. **"Specialist agents do not pay on real code" (packet §1 headline)
    generalizes one agent × four tasks.** The ledger's S11 UNVERIFIABLE is
    the calibrated statement; the headline is not. — **CONFIRMED** (S1-luna)
19. **Telemetry has no data policy.** Capture modes that record prompts/code
    are live-tested features (S8/S9), but there is no default-off statement,
    retention/deletion rule, or redaction pipeline; `.gitignore` excludes
    only eval scratch dirs and `__pycache__`. — **CONFIRMED** as a policy
    gap (S3). One S3 detail is **WRONG**: it claims
    `wiki/telemetry/events.jsonl` exists in the tree; the directory exists,
    the file does not (in phase-2 @ 3556e46).
20. **Cost governance is advisory.** AGENTS.md §7 asks agents to state costs;
    nothing enforces a budget — S16's $4.63-vs-~$4 overshoot is the
    in-repo instance. Measurement exists; containment does not.
    — **CONFIRMED** facts, severity is **OPINION** (S3)

### Where Copilot was wrong or overstated

- S1-haiku finding #1 quotes the packet's "Orientation REPLICATED" as if it
  framed the Rich result. It does not: the line (packet §1) describes the
  same-day second NetworkX batch. The generalizability point stands; the
  quote's target does not. — citation **WRONG**, substance CONFIRMED.
- S1-haiku finding #2 supports the S16 ceiling point with a packet quote
  that is actually the S11 specialist text. — citation **WRONG**, substance
  CONFIRMED from `evals/results/2026-09-30-P2-copilot-ab.md`.
- S1-haiku finding #3 (E5): the correction and PARTIAL verdict are real and
  in-file; its further claim that the E5 criterion "was not pre-registered
  tightly enough" is **OPINION** — pre-registration status is not
  established either way by the cited file.
- S1-luna calls an as-shipped MCP path "PARTIAL/REFUTED in the tested
  environment" for S14: Playwright's failure is root-sandbox-specific, so
  REFUTED overstates it; PARTIAL (the project's own label) is the accurate
  term. The S14 calibration finding stands without the stronger word.
- S3's maturity frame assumes team adoption is the bar. The repo is a
  one-author research workspace mid-demo; several "missing" items (CI,
  release trains) are sequencing choices, not defects. The safety-relevant
  gaps (##1, 3, 4, 17 above) stand regardless of that frame.

## What Copilot caught that this project's own reviews missed

Own reviews (refutation pass, docs fact-check, external-signal sweep,
prompt audit, merge-readiness work) already held: the Rich null, the S16
ceiling, Playwright PARTIAL, evidence living outside the repo, orientation
cost framing. Copilot converged on those independently — and added:

1. Adapter stripping canonical `model_hint`/`tools_hint` + missing
   `include-custom-instructions: true` (finding #1). Port verification
   invoked the emitted agents; nobody diffed emitted frontmatter against
   canonical intent.
2. The stale "no hook loader" mechanism surviving in the **ledger** and in
   `adapters.py:128` after E4 corrected it (finding #2). The external sweep
   fixed the packet's wording only.
3. Installer config destruction incl. the silent `{}` reset on malformed
   settings (finding #4). No prior review read `install_hooks()` as a
   data-loss path.
4. The R2 wording-dependence of a headline discordant pair (finding #5) —
   disclosed in the results file, never promoted to the headline's risk.
5. S8's 60KB over-cap assertion lacking a demonstrated over-cap capture
   (finding #11), and C1/C2's PROVEN-on-research class error (finding #12).
6. README/setup fiction: missing clone command, nonexistent
   `canonical/plugins/` + `adapters/` in the depicted tree, phantom
   toolchain files, self-contradictory "done" criteria (findings #13-15).

## Ratings (Copilot's, recorded not endorsed)

- Evidence discipline: **6/10** — independently from both claims-audit
  sessions (different models). Strengths named: pre-registration, oracle
  validation, disk grading, retained corrections, honest nulls. Deductions:
  headline calibration, pooled framing, stale ledger rationale, evidence
  custody.
- Project maturity: **3/10** (S3) — "demo/research-grade yes, team-grade
  no," driven by findings #1, #3, #4, #17 and the absence of CI/release
  discipline.
