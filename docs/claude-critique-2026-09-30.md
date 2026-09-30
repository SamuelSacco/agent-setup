# Claude (Opus) critique — 2026-09-30
- Reviewer: Claude Code 2.1.285, model claude-opus-5-5 (--model opus), --bare API-key mode
- Branch: critique/claude off phase-2 @ 3556e46
- Method: claims traced to cited evidence on disk; narrative numbers traced to evals/results/; canonical/ reviewed read-only (a parallel stream is editing five canonical files; this review reports on them but does not edit canonical/)
- Severity scale: BLOCKER (merge should not proceed), MAJOR (claim/statement wrong or unsupported as worded), MINOR (imprecision), NOTE (observation)

## Pass 1 — Claims audit (docs/claims-ledger.md)

### Pass 1A — S1–S9 (incl. sub-rows S6a, S6b)

**Claims audited: 11 (S1, S2, S3, S4, S5, S6, S6a, S6b, S7, S8, S9) · clean: 3 · flagged: 8**
Findings: 1 BLOCKER · 5 MAJOR · 5 MINOR · 2 NOTE

---

### [BLOCKER] S4 — Ledger states a Copilot mechanism and verdict that its own cited evidence file retracts
- **Ledger (docs/claims-ledger.md:26):** "Copilot: REFUTED on installed CLI v1.0.89 — binary contains no hook loader; 0/5".
- **Evidence:** `evals/results/2026-09-30-E4.md:53-87` (addendum, ~01:45 ET) says the "no hook loader" attribution was *wrong*: "the loader machinery is in the bundle" (:59-60); hooks **fire** when the directory is trusted via `COPILOT_ALLOW_ALL=true` (:68-71); the original 0/5 happened because the run was "untrusted, not hookless" (:66-67). The real gap is that `postToolUseFailure` never fires for shell failures, because the shell tool reports `"resultType":"success"` even on exit 127 (:72-77). The file closes: "S4's Copilot leg changes from REFUTED to PARTIAL-with-mechanism" (:86-87).
- **Propagation:** the retracted wording is still in `scripts/adapters.py:125-130` ("REFUTED … the binary contains no postToolUseFailure/sessionStart hook loader") and `docs/demo-backup/e4-events.md:13-14` ("no hook surface in the binary"). The adapter still emits only `postToolUseFailure` (adapters.py:136). The addendum shows that event does not catch shell failures, and the fix it identifies (`postToolUse` + parse exit-code text) is "identified, not yet built" (E4.md:82-83).
- **Why BLOCKER:** the ledger's rule (ledger:45-47) is that verdicts change only through evals, in the same change as the result. Here the eval changed the verdict and the ledger did not follow. A reader of the gate artifact gets a mechanism the evidence explicitly withdraws.
- **Correction:** replace the Copilot leg with: "Copilot v1.0.89: hooks load only in a trusted directory (`COPILOT_ALLOW_ALL=true`); `sessionStart`/`preToolUse`/`postToolUse` fire; `postToolUseFailure` did not fire for shell failures (shell reports success on non-zero exit); 0/5 captured as built; capture path = `postToolUse` + exit-code parse, not built. `postToolUseFailure` for non-shell tools untested." Fix the adapters.py comment and the demo-backup line in the same change.

### [MAJOR] S5 — "probe inputs −51%" counts only uncached input tokens; total input processed fell ~2%
- **Ledger (:27):** "token axis PROVEN (38% cut, probe inputs −51%)".
- **Evidence:** the 10,421 / 5,083 figures (E5.md:15-16, :36-37) are the `usage.input_tokens` field alone. From the transcripts' `usage`: all-notes = 10,421 fresh + 18,071 cache-create + 42,917 cache-read = **71,409**; active-only = 5,083 + 9,707 + 55,229 = **70,019**. That is a **−1.9%** drop in total input context. Metered cost did fall ~40% ($0.0568 → $0.0343), and turns fell from 44 to 14.
- **Correction:** drop "probe inputs −51%" or restate it as "uncached input −51%; total input context −2%; cost −40%". The 38% orientation figure is a separate measurement (see MINOR below).

### [MAJOR] S5 — The "narrowed claim PROVEN" is a post-hoc re-scope; the pre-registered consequence of failing was not carried out
- **Ledger (:27):** "broad quality claim REFUTED as scored … narrowed claim PROVEN (6/6 active-scope correct …)".
- **Evidence:** the pre-registered test (`evals/tasks/E5-context-cost.md:6-8`) has one quality bar: a drop of ≤1 on 10 questions. The same file says what happens on failure: "If quality drops > 1, the retirement rules are too aggressive — loosen them and record the change in `data-model.md`" (:19-20). The drop was 4 (E5.md:39). `wiki/data-model.md` has not changed since the initial commit 2294652. The retirement rules (data-model.md:72-79) were not touched. Instead a new, narrower claim was defined after seeing the results and marked PROVEN on n=6 synthetic frontmatter facts (E5.md:53-55).
- **Correction:** S5 = "REFUTED at the pre-registered bar (drop 4 > 1); token axis met." Record the 6/6 active-scope observation as a descriptive result, not PROVEN, unless it is pre-registered and re-run (ideally on the real wiki, as E5.md:53-55 already asks). Either carry out the pre-registered data-model.md remediation or record why it was waived.

### [MAJOR] S5 — The 6/10 score can't be audited: probe questions and answer key are not on disk, and one answer doesn't fit the stated scoring
- **Evidence:** the ten probes and their ground truth are nowhere in the repo. I searched `scripts/seed_wiki.py`, `evals/`, `docs/`, and the transcripts (which hold only the `result` text). E5.md:18-21 names exactly four archived-only facts that were answered "not recorded" (Q3, Q6, Q7, Q8 in the transcripts). But on **Q4** the all-notes run answered "**15**" (and listed the 15 archived notes), while the active-only run answered "**0**". If Q4 is scored against corpus truth, as the correction section (E5.md:25-32) says every question was, then "0" is wrong. That makes the score 5/10, not 6/10, and the "6/6 active-scope" count includes an answer that differs from the full corpus. The "grep-verified" check (E5.md:31-32) counts "not recorded" strings and would not catch a wrong number.
- **Correction:** commit the probe list and answer key. Re-score Q4 explicitly. State whether it is corpus-scoped (then active-only = 5/10) or directory-scoped (then say the scoring frame is mixed).

### [MAJOR] S6b — The Copilot failure happened under different permission conditions than S6a's pass; the ledger presents it as "the same bounded task"
- **Ledger (:30):** "Copilot `backend` agent completes the same bounded task — REFUTED (pilot)".
- **Evidence:** the Copilot transcript shows the subagent's writes and commands being blocked again and again: "Permission denied and could not request permission from user" (`2026-09-30-E6-pilot-copilot-transcript.txt:38,41,56,62,78,84,94,105`, …). That is the same approval boundary that blocked Claude's pilot (E6-pilot.md:18-21). Claude got a rerun with pre-approved writes, and S6a is explicitly scoped "when writes are pre-approved". Copilot was never re-run with the equivalent (`--allow-all-tools` / `COPILOT_ALLOW_ALL=true`). E6-pilot.md:35-36 calls the root cause "UNVERIFIABLE from this run alone", but the transcript shows it. The fabrication finding is real: a made-up pytest block ending "22 passed in 1.23s" (transcript:430), then `Changes +0 -0` (:499). One wording issue, though: the parent's final summary says "Expected Test Results … 22 passed in ~1.2s … All tests would pass" (:480-483), which is hedged, not a direct claim that tests ran.
- **Correction:** "REFUTED under default (non-pre-approved) permissions, n=1: writes denied, agent then reported fabricated test output; not re-run with writes pre-approved, so not comparable to S6a." Queue the pre-approved rerun before any parity statement is made.

### [MAJOR] S2 — The claim is broader than one direction, one session, and recall-only probes
- **Ledger (:24):** "A session in tool A is continuable by tool B … PROVEN".
- **Evidence:** `evals/results/2026-09-30-E2.md:10-16`. Only one direction was run (Copilot → Claude), on one session, with Claude on Haiku (transcript `modelUsage`: claude-haiku-4-5-20251001). The Copilot model was not recorded (GitHub-hosted, AI Credits). The probes are read-only recall questions (E2.md:14), and tool B never continued any work. The pre-registered step 1 required "the session log and at least one hardened note are written" (`evals/tasks/E2-cross-tool-continuity.md:10-11`), but none was ("no durable workspace note needed", E2 transcript answer 4; E2.md:26-28). Probe 4 therefore became a "none" trick question rather than a test of note retrieval. The baseline control is weaker than stated: the baseline transcript notes the wiki files are "marked as deleted in git status", so the session record could be recovered from git. The clean 5/5 "not recorded" depended on the model not looking, not on the information being gone. An aborted baseline run ($0.055, E2.md:37-38) is also left out of the ledger.
- **Correction:** "PROVEN for Copilot→Claude (Haiku), n=1 session, 5 recall probes; reverse direction and actual work continuation untested; no hardened note written (pre-registered step deviation); baseline removed wiki/ from the working tree but not from git history."

### [MINOR] S1 — "Claude Code did the same" overstates: the Claude run stopped at a denied write, and the pre-registered listing step was never done for Claude
- **Ledger (:23):** "Copilot invoked `session-harden` by name and executed its body; Claude Code did the same".
- **Evidence:** in `2026-09-30-E1-claude-transcript.json`, `permission_denials` holds the session-file Write and `result` = "I need permission to write the session file…". E1-claude.md:12 records it as BLOCKED. The procedure was followed up to the write, as the drafted file content in the denial shows, but not executed to the end. The pre-registered PASS condition is "both tools **list** `session-harden` as an available skill" (`evals/tasks/E1-install-parity.md:6-7`). Claude never listed skills; invocation was used as a stand-in (E1-partial.md:10). The result-only transcript also has no tool-use trace, so "invoked by name" rests on the prose. Scope left out of the ledger: one skill, Claude on Haiku 4.5, Copilot model not recorded, and no Copilot transcript on disk (evidence is prose only, E1-partial.md:17-38).
- **Correction:** "…Claude Code (Haiku) invoked it and followed the body up to the session-file write, which was blocked by the headless permission prompt; discovery inferred from invocation (no listing surface)."

### [MINOR] S5 — The 38% token cut is a chars/4 estimate, and the corpus has no "stale" notes
- **Evidence:** `evals/results/2026-09-30-E5-partial.md:5,14` ("chars/4 est.", "chars/4 is an estimate"). The ledger says "PROVEN (38% cut)" without mentioning the estimate. The claim and the task say "archived/stale", but `scripts/seed_wiki.py:34-39` writes 15 `status: archived` notes and 0 `stale` notes (grep of the fixtures: 15 archived, 0 stale).
- **Correction:** "38% cut (chars/4 estimate)"; narrow the claim wording to "archived" notes.

### [MINOR] S6a — The cited transcript path no longer exists; the evidence survives only in git history
- **Ledger (:29) cites** `evals/scratch-e6-claude/run1.json` (via E6-rerun-claude.md:32). That directory was deleted and gitignored in 5226e5c. I recovered it from **268efcb**, and it checks out: `ratelimit.py` 1,928 B, `test_ratelimit.py` 6,233 B with 13 `def test_`, run1.json = $0.0766674, 11 turns, Haiku 4.5, no permission denials. Not preserved: the output of Helm's independent `pytest` re-run ("13 passed in 8.18s"), and whether the run used `--agent backend` (the invocation in E6-rerun-claude.md:12-13 lists only the permission flags). The model (Haiku) is missing from the ledger.
- **Correction:** cite `268efcb:evals/scratch-e6-claude/`, record the exact command line, and add "Haiku 4.5".

### [MINOR] S7 — "model constant, harness the only variable" holds only for BYOK runs; earlier cross-tool claims were not BYOK
- **Evidence:** `evals/results/2026-09-30-byok-probe.md:13-22` is a single "OK" probe. It establishes the capability. But the S1 and S2 Copilot legs ran GitHub-hosted and were billed in AI Credits (E1-partial.md:34-35; E2.md:10-13), with the model not recorded. So the parenthetical does not carry over to those results. "Billing went to Anthropic" is inferred from a missing footer line. Stronger evidence is already on disk and not cited: `~/agent-logs/copilot/otel.jsonl` spans carry `gen_ai.provider.name=anthropic` / `server.address=api.anthropic.com` (otel-instrumentation.md:48-49).
- **Correction:** "(when Copilot runs BYOK; the S1/S2 Copilot legs were GitHub-hosted)". Cite the OTel provider attributes as the routing evidence.

### [MINOR] S8 — Prerequisites and a recorded caveat are missing; the >60 KB support isn't in the cited file
- **Evidence:** the run used `CLAUDE_CODE_ENABLE_TELEMETRY=1 OTEL_LOGS_EXPORTER=console OTEL_LOG_RAW_API_BODIES=file:…` (otel-instrumentation.md:13-15), but the ledger presents the single env var as sufficient. The cited `--bare` body is 5,417 B (:17), well under 60 KB. The "size-complete past the 60KB cap" support is the 82,441 B `raw-default` request, which is recorded only in `hidden_files/research/2026-09-30-otel-debate-factcheck.md:76-78`, and that file is not cited. The same factcheck file records a caveat the ledger leaves out: `body_ref` is "UNVERIFIABLE in the local artifacts" (:85-89), and `index.jsonl` requires v2.1.274+ (:70). On disk, `~/agent-logs/claude/raw{,-default}/` match: 5,417 B and 82,441 B requests, `index.jsonl`, `input_tokens: 1866`, `<REDACTED>` thinking text in both responses. These artifacts sit outside the repo and are not committed.
- **Correction:** list the required env vars, add the factcheck file to the evidence column, and add "body_ref pointer unverified locally". Consider committing the index.jsonl files.

### [NOTE] S3 — Correctly UNVERIFIABLE; S12 must not be read as covering it
- E3 (`evals/tasks/E3-wiki-value.md`) was never run. S12's orientation arm is a frozen `CLAUDE.md` text with no wiki (`evals/results/2026-09-30-P2-realcode-prereg.md:172-174`), even though S12's claim says "AGENTS.md/wiki context". No PROVEN row currently supports wiki orientation as such.

### [NOTE] S9 — The "alone auto-enables" half rests on docs, not on the artifact
- Both captured runs in `~/agent-logs/copilot/otel.jsonl` have content capture on (4× `gen_ai.system_instructions` across 2 runs). No artifact shows `COPILOT_OTEL_FILE_EXPORTER_PATH` set without the content flag. The local help text supports it (`copilot-help-monitoring.txt:33-34`). "16-record" is correct for run 1: records 0-15 are 2 spans + 14 metrics. The file has 33 lines because run 2 adds a cache_read metric.

---

**Verified clean (S1–S9)**
- S3 — `evals/tasks/E3-wiki-value.md` (UNVERIFIABLE, matches: eval not run; see NOTE)
- S6 — `evals/tasks/E6-agent-parity.md`; E6-rerun-claude.md:28-30 (UNVERIFIABLE, matches: no blind grid, 1 of 3 agents, 1 of 3 tasks)
- S9 — `evals/results/2026-09-30-otel-instrumentation.md:44-57`; `hidden_files/research/copilot-help-monitoring.txt:33-34,135-138`; `~/agent-logs/copilot/otel.jsonl` (see NOTE)

## Pass 2 — Narrative audit (packet + addendum)

### [MAJOR] packet:4-5 — cited source files are not on this branch; ~15 packet numbers can't be traced in-repo
- Claim: "Sources in `evals/results/2026-09-30-P2-*` and `hidden_files/research/2026-09-30-P2-*` on this branch."
- Evidence: this branch has exactly one `hidden_files/research/2026-09-30-P2-*` file (`P2-ecc-mining.md`). The files behind the numbers below exist only in unmerged worktrees under `~/workspace/phase2/*/hidden_files/research/`:
  - `P2-onboarding.md` covers packet:83-93: "0 decisions, 2 unavoidable human actions" (onboarding:66), "30 s warm" (:98), "1m58 s cold" (:69), "Claude 19 s, Copilot 41 s" (:22,41), "32 paths" (:25), "$0.004–0.012" (:88), and the spend line's "onboarding $0.08" (:127-129).
  - `P2-roster-v2.md` covers packet:60-61: "~300" (roster:243), "~546" (:96), "~3.5k" (:97, ~3,542).
  - `P2-skills-ecosystem.md` covers packet:42 "683K installs" (:96,146) and the ToxicSkills block at packet:40-41 (:112-113). That block is primary-checked only in off-repo `~/workspace/phase2-external-signal-2026-09-30.md:77`.
  - `P2-copilot-surface.md` covers packet:67-79.
  Every value I checked matches its off-branch source. None of them can be checked from the repo.
- Correction: commit the four research files onto `phase-2` before merge, or reword packet:4-5 to name the worktree paths honestly.

### [MAJOR] packet:83-85 — the headline adoption asset `quickstart.sh` isn't in the tree
- Claim: "quickstart.sh prototype: one command, 0 decisions… Fresh-sim: 30 s warm; 1m58 s cold".
- Evidence: `scripts/` holds `adapters.py install.sh run-eval.sh run_eval.py seed_wiki.py sidecar.sh`, with no quickstart. Commit `6cb12f5` (branch `origin/audit/merge-readiness`, NOT an ancestor of HEAD) already logged this as "1 blocker (quickstart.sh claimed, not shipped)", and that fix never reached this branch.
- Correction: ship the script, or change the claim to "prototyped in the `phase2/onboarding` worktree, not merged". Also make sure the `audit/merge-readiness` fixes land before this merge.

### [MINOR] packet:60 — "~300 tokens" is an estimate listed under "all live-invoked"
- Evidence: `P2-roster-v2.md:243` "Description rent of the 6: est. ~300 tokens". The ~546 and ~3.5k figures are chars÷4 (`:96-97`, 2,186 and 14,169 chars). None of the three is an API token count, unlike the measured context-rent section at packet:97.
- Correction: "est. ~300 tokens (chars÷4) of description rent (vs ~546 … ~3.5k, same method)".

### [MINOR] addendum:33 — Copilot token range stated per run, but it holds only for T1/R2 *(fixed)*
- Evidence: `P2-copilot-ab.md:80` "(1.7–2.0M input tokens on T1/R2)". T3 Copilot base was 416.2k input (`P2-realcode-ab.md:34`), and T3 +orient cost $0.63 (`P2-copilot-ab.md:30`), which works out to ~0.6M.
- Correction: applied, see Fixes.

### [MINOR] packet:40 vs addendum:82 — "36.8%" contradicts "numbers exact"
- Evidence: the primary figure is 36.82% (1,467/3,984; `~/workspace/phase2-external-signal-2026-09-30.md:77`). The same file, at `:19`, says "Use exact figures: … 36.82%". The addendum says the packet's numbers are "exact vs Snyk primary", but the packet prints 36.8%. The value is correct; the precision claim is wrong. Not fixed, because the source is off-repo.
- Correction: packet:40 "36.82% ≥1 flaw".

### [NOTE] packet:21 — misquoted self-report *(fixed)*
- Evidence: `P2-realcode-ab.md:71` reads "All 106 existing tests pass." The packet puts "All 106 tests pass." in quotation marks.

### [NOTE] packet:108 — "V1 evals: ~$1.03" has no traceable sum
- Evidence: no results file totals V1 spend, and I did not re-derive it from the E1–E6 files. Either cite the sum or drop the figure.

### [NOTE] Upstream of packet:14 — the results file contradicts its own table
- `P2-realcode-ab.md:57-58` says the agent arm "cost more than base on 4/4 tasks". Its own table shows T1 +agent $0.289 < base $0.483 (`:17-18`), so the real count is 3/4. The packet uses only the aggregate (+8.5%), which is correct, so the packet is unaffected. The results file needs the fix; it's outside my edit remit.

### Verified clean
3/4·73·$1.164 / 3/4·113·$1.263 / 4/4·77·$0.967; +55% turns / +8.5% cost; replication 3/4 vs 4/4, $0.898 vs $0.662, $1.56; combined 8/8 vs 6/8; 11/12 vs 9/12 (realcode:345); Rich 3/4 vs 3/4, U3, ~26.6k LOC, 9d8f9a37, prereg d85c6e5 (git), $1.88; "22 passed"; 201 s (port-verif:52-67); 12 agents / 8 skills / 5 MCP (port-verif:9); 668/19/223/426 (ecc-mining:31,45); 1,866 / 14,510 / 20,589 / 23 tools / ~5.9–6.2k / ~7.7–8k (otel:31,42,68; binary-forensics:53,75); W3 $5.35, matrix $0.65, W5 $0.12, port probes $2.7768, packet sum $10.54, balance 18.23−10.54≈$7.7; Copilot $4.63, 3/3 base, 3–9× (max 9.2×), +orient above base on both pairs; run-eval PASS 1/1, 11 turns, $0.103, 151 s (RUN file); 3m50s (feedback-loop.md:101); addendum all-in 10.54+1.883+4.63+0.103 = $17.16 ≈ $17.2; 2,796 lines / 12 SUSPECT / 0 contradictions (off-repo prompt-audit:3,32); ToxicSkills 3,984 / 13.4% / 76 (off-repo).

### Fixes applied
1. `docs/phase2-packet-2026-09-30.md:21`: `reported "All 106 tests pass."` → `reported "All 106 existing tests pass."` (source `P2-realcode-ab.md:71`)
2. `docs/phase2-addendum-2026-09-30.md:33`: `(1.7–2.0M input tokens/run, mostly cached,` → `(1.7–2.0M input tokens on T1/R2 runs, mostly cached,` (source `P2-copilot-ab.md:80`)

---

## Provenance and reconciliation (orchestrator note)

Two independent Opus passes audited the claims ledger in parallel runs: Pass 1A above (S1–S9, kept) and a full-ledger pass whose S1–S9 section was overwritten in a write race between the two CLI processes (both outlived their harness wrappers). Its S10–S17 findings were recovered verbatim from the orchestrator's read of the file before the overwrite and are restored as Pass 1B below. Where the two passes disagree on S1–S9 severity, Pass 1A (above) governs — it carries the stronger evidence (e.g. S4 as BLOCKER, via propagation into `scripts/adapters.py` and `docs/demo-backup/`). One Pass-1B-era claim was itself wrong and is corrected in the verification section (S8 raw-body artifact).

**Totals across passes:** 2 BLOCKER · 9 MAJOR · 11 MINOR · 6 NOTE (claims + narrative) · setup soundness: 3 HIGH · 9 MEDIUM · 5 LOW.

## Pass 1B — Claims audit S10–S17 (restored)

### [BLOCKER] S12 — "Orientation (AGENTS.md/wiki context)" PROVEN, but neither AGENTS.md nor the wiki was tested, and S3 says the same idea is UNVERIFIABLE
- Claim (ledger:36): "Orientation (AGENTS.md/wiki context) improves task success on real code — PROVEN".
- Evidence: the treatment arm was "a `CLAUDE.md` at the checkout root containing the frozen Orientation text" — a hand-written layout-and-conventions note of about 40 lines, specific to NetworkX (`evals/results/2026-09-30-P2-realcode-prereg.md:172-174`, appendix at `:224` onward). The Rich arm used another hand-written file, `assets/orientation.md`, placed the same way (`P2-realcode-ab.md:277-279`). None of the runs used this repo's AGENTS.md, its wiki, or `install.sh` output. Ledger S3 "Wiki orientation improves task success vs no-wiki baseline" sits at UNVERIFIABLE (ledger:25): the ledger calls wiki orientation PROVEN in one row and UNVERIFIABLE in another.
- Scope the claim leaves out: all 20 runs were Claude Code 2.1.285 with `claude-haiku-4-5-20251001` only (`P2-realcode-ab.md:7-8, 213-214`). The same test on Copilot came out UNVERIFIABLE (S16).
- Correction: reword S12 to "A hand-written, repo-specific orientation file (CLAUDE.md) improved Claude Code + Haiku 4.5 task success on NetworkX (n=8, 2 discordant pairs); null on Rich (n=4)". Drop "AGENTS.md/wiki" from the claim, or keep S12 PROVEN only for the narrowed wording. S3 stays the open question for the wiki itself. Any deck or packet line that reads "the wiki/AGENTS.md improves success" has to change with it. **[Orchestrator: CONFIRMED — see verification section.]**

### [MAJOR] S12 — the "pre-registered combined rule" was written after the NetworkX result, so a null second codebase could not move the verdict
- Claim (ledger:36): "combined verdict PROVEN stands under the pre-registered combined rule".
- Evidence: the Rich prereg commit `d85c6e5` comes after the n=8 NetworkX result commit `025dea6` (`git log`). The rule (`P2-realcode-ab.md:303-309`) says PROVEN if combined orientation > combined base AND Rich is not REFUTED. NetworkX was already +2, so any Rich result except a Rich loss keeps PROVEN; a tie or null on the new codebase could never downgrade it. The whole effect is 2 discordant pairs out of 12 tasks; a two-sided sign test on 2/2 gives p = 0.5. One of the two pairs (R2) turned on exception-message wording ("No nodes in graph" vs the test's `null graph` match, `:192-199`). The results file itself says the combined weight "rests on" NetworkX (`:347-351`).
- Correction: state it as "PROVEN at a pre-registered bar on one codebase (NetworkX); did not replicate on a second codebase (Rich, null)". Say explicitly that the combined rule was set after the first-codebase outcome was known. Do not describe the result as generalizing to "real code". **[Orchestrator: CONFIRMED.]**

### [MAJOR] S14 — "The 19 ECC ports … invocable in BOTH tools" PROVEN, while one port's call is REFUTED in both tools as shipped
- Claim (ledger:38): "19 ECC ports … discoverable and invocable in BOTH tools … PROVEN".
- Evidence: playwright (one of the 4 MCP ports) is "PARTIAL … call REFUTED as-shipped in this sandbox" in both tools (`P2-port-verification.md:101`). It worked only after sandbox provisioning (`npx playwright install chrome`) plus a modified `--no-sandbox` config (`:108-113`). On a non-root machine the as-shipped config is "UNVERIFIABLE from here" (`:112`). So 18/19 ports are invocable as shipped, and the 19th is unproven in any as-shipped setting. In Copilot, sequential-thinking and filesystem-wiki passed only on a warm cache (`:98-99, 123-130`). Skill probes were "load-and-stop" and show "discovery + invocation, not full workflow completion" (`:90-91`). The Copilot agent column is task delegation, not the agent run as the session (`:14-15`).
- Correction: **PARTIAL**, or reword to "18/19 invocable as shipped in both tools; playwright UNVERIFIABLE as shipped (REFUTED in root sandbox)". A carve-out inside a PROVEN verdict does not cover a REFUTED item that the claim wording includes. **[Orchestrator: CONFIRMED; ledger downgraded.]**

### [MINOR] S13 — the post-fix evidence is cited to the wrong file and shows listing, not invocation
- Claim (ledger:37): "adapter now emits `mcpServers` + `servers` (commit 4ed071c), Copilot lists all 5 workspace servers".
- Evidence: the cited `P2-install-matrix.md` predates the fix; it shows 2 probe servers, and invocation only through the root `.mcp.json` (`:35, 194-203`). "Lists all five" comes from `P2-port-verification.md:136-137`. That run had both root `.mcp.json` and dual-key `.github/mcp.json` present, so the fixed file was never tested on its own. The isolation test covered `mcpServers`-only, not dual-key (`install-matrix:201`). The PROVEN verdict holds as worded, through the root `.mcp.json`.
- Correction: add `P2-port-verification.md` to the evidence and say "dual-key `.github/mcp.json` not isolation-tested; Copilot invocation proven via root `.mcp.json`".

### [MINOR] S16 — cost ratios compare Copilot upper bounds with Claude's metered cost, and "opposite the Claude direction" is only half true per pair
- Claim (ledger:40): "Copilot converts at 3–9× Claude's per-task cost; $4.63 of ~$4 cap spent… +orientation cost/wall ran above base on both completed pairs, opposite the Claude direction".
- Evidence: Copilot figures count cached input at the full rate. "Nearly all input tokens were cached (T1 +orient: 2.0M of 2.0M)" and the file calls them "upper-bound estimates, not billed amounts" (`P2-copilot-ab.md:39-43`). The Claude figures are metered cost with cache discounts, so 3–9× is an upper bound and not like-for-like, and $4.63 is converted, not spent. Per pair, Claude's T3 orientation arm also cost more than base ($0.114 vs $0.075, `P2-realcode-ab.md:24-26`). The Claude "direction" only holds for totals.
- Correction: "≤3–9× (upper-bound conversion vs metered)"; "$4.63 converted"; "opposite the Claude *aggregate* direction".

### [MINOR] S17 — "end-to-end" was exercised for one tool, one arm, and the easiest task
- Claim (ledger:41): "reproduces a disk-graded verdict end-to-end from a task package — PROVEN".
- Evidence: one run, `--tool claude`, arm `base`, on nx-t2 (`RUN-nx-t2-…md:11-12`). T2 is the task every Claude arm passed in W3 (`P2-realcode-ab.md:21-23`), so the proof run never shows the runner producing a FAIL verdict. The runner implements a Copilot branch (`scripts/run_eval.py:163-172`) and `agent`/`orient` arms (`docs/feedback-loop.md:111-113`); none were exercised. The ledger's carve-out lists only clone and venv. (Also: `docs/feedback-loop.md:115-117` has the "### Proof run" heading twice.)
- Correction: add "claude/base only; copilot and agent/orient arms and a FAIL verdict not exercised".

### [NOTE] Cross-cutting — most P2 primary evidence is off-repo on one VM
- The run envelopes, diffs, markers, spend ledgers, and OTel captures behind S8, S9, S12–S17 live in `~/workspace/p2/**`, `~/agent-logs/**`, and gitignored `evals/scratch-*`. They exist on this VM, and spot checks matched (W3, replication, and Rich `ledger.tsv` agree with the results tables). But a reviewer who has only the repo gets narrative md files. The ledger header says "Updated by eval runs — never by opinion", and from inside the repo that is currently checkable only for S2/S4/S5, which have in-repo transcripts. Recommend committing at least the per-run `ledger.tsv` files and result envelopes.

### Verified clean (S10–S17)
- S10 — `evals/results/2026-09-30-otel-instrumentation.md` (14,510 / 9,547÷14,509 = 66% / 23,655÷4 ≈ 5.9k re-derived)
- S11 — `evals/results/2026-09-30-P2-realcode-ab.md:40-58` (113/73 = +55%, 1.263/1.164 = +8.5%; matches w3 ledger.tsv)
- S15 — `evals/results/2026-09-30-P2-port-verification.md:49-71`

---

## Pass 3 — The CLAUDE.md question, both sides

(From the final Opus pass; the repo ships `CLAUDE.md` containing only an `@AGENTS.md` bridge plus a short Claude-only annex, while `AGENTS.md` claims a tool-agnostic design, and Claude Code ≥ 2.1.277 loads AGENTS.md natively.)

### Keep the bridge
- It works everywhere. The `@AGENTS.md` import has no version floor. Native read needs Claude Code >=2.1.277 (>=2.1.281 off the direct API, not on Bedrock/Vertex/Foundry at launch) (P2-claudemd-drop, Verdict).
- It avoids the silent trap. Deleting the file only helps if no `CLAUDE.md`/`CLAUDE.local.md` exists in cwd or any ancestor. Arm C lost the shared canary 2/2 and the model never said anything was missing. Contamination runs showed a parent-dir `CLAUDE.md` alone is enough to cause this.
- It keeps telemetry. `InstructionsLoaded` fires for an imported AGENTS.md but not for a natively read one (research §2), and AGENTS.md §6 depends on hook events.
- It costs little: one import line, measured never to double-load in Claude (arm A 2/2). The Claude-only annex needs a home anyway.
- Shipping it doesn't depend on per-user state. Arm D's fix sits in `~/.claude/settings.json` and can't ship with the repo.

### Delete CLAUDE.md
- It goes against the stated design. AGENTS.md:3 says "tool-agnostic", yet the repo still ships a vendor-named root file for the one tool that now reads AGENTS.md natively (arm B 2/2, loader debug line).
- Copilot loads it too. `copilot instruction list` shows root `CLAUDE.md` as a model source (E1 addendum; tips-copilot.md:24). Every Copilot session then gets "Claude Code only" text pointing at `/context` and `/advisor`, plus a bare `@AGENTS.md` line. Nobody has tested whether Copilot expands it (a double-load) or ignores it (noise). "Never double-loads" is PROVEN only for Claude.
- The annex is 2 pointers. `.claude/rules/` (Claude-only, loads at launch) is the right home for it, which leaves nothing that needs CLAUDE.md.
- The hook argument is weak. The shipped hook is `PostToolUseFailure` (.claude/settings.json). Nothing in the tree consumes `InstructionsLoaded`, so "hook loss" breaks nothing that exists today.
- The ancestor trap cuts both ways. Keeping the bridge doesn't protect a user whose parent directory has its own CLAUDE.md either. That file loads in addition, so the only difference is which failure you get.

### Reviewer lean
Keep the bridge for now. The version/surface floor and the silent suppression are PROVEN risks. Delete's strongest point (Copilot ingesting Claude-only text) is real but only costs tokens.
The deciding condition: if everyone who uses this repo is on Claude Code >=2.1.281 with the agents-md plugin enabled, delete and move the annex to `.claude/rules/`. Until the repo can pin or check that, keep it.

## Pass 4 — Setup soundness (canonical/ + emitted configs)

Reviewer severity labels from this pass kept as written (HIGH ≈ MAJOR tier, MEDIUM, LOW ≈ MINOR tier). Excluded as already known to a parallel stream: researcher / security-review / tdd setup script / 80% / code-reviewer MUST / 15-min re-verify.

### [HIGH] scripts/adapters.py — tool restrictions are dropped, so every agent gets every tool
Evidence: canonical/agents/planner.md:5 and code-explorer.md:5 declare `tools_hint: [read, search]`. code-reviewer.md:5 and security-reviewer.md:5 declare `[read, shell, search]`. adapters.py:79 and :84 build frontmatter from `name` and `description` only. Emitted `.claude/agents/planner.md` has no `tools:` line, so Claude falls back to all tools (Edit/Write/Bash included), and so does Copilot's `.agent.md`. The adapter's own docstring (adapters.py:9) says it emits `model, tools`. It doesn't.
Fix: translate `tools_hint` into each tool's `tools:` allowlist, and fail the install on unknown hints. **[Orchestrator: CONFIRMED — see verification.]**

### [HIGH] AGENTS.md — a mandatory session ritual runs on every session, however small
Evidence: AGENTS.md:9 "At the start of every session" means 3 file reads plus stating intent. :16 "Do not skip orientation to 'save time.'" :20 "Every session follows this lifecycle": create a session file, :28 "Append turn entries as you work", then a 4-step hardening at :33-37. A one-line question costs several tool calls and wiki writes. Nothing in evals/ shows this pays off; it is stated, not measured.
Fix: trigger the lifecycle only for sessions that change files (or make it opt-in), and keep hardening in the `session-harden` skill instead of the always-loaded root file.

### [HIGH] canonical/hooks/failure-capture.json + scripts/sidecar.sh — raw failure payloads go into a git-tracked file
Evidence: sidecar.sh:23-25 appends the full hook stdin (Claude's `PostToolUseFailure` payload includes `tool_input`: full shell commands, file contents on failed writes) to `wiki/telemetry/events.jsonl`. `git ls-files` shows that file **is tracked**, and `.gitignore` has no rule for it. A failed authenticated curl ends up committed. The filesystem-wiki MCP server can read and write the file too. Non-JSON stdin is inserted unquoted (:25) and corrupts the JSONL.
Fix: gitignore `wiki/telemetry/`, keep only an allowlist of fields (tool name, exit code, error class), and validate or quote the payload. **[Orchestrator: CONFIRMED — file is tracked, no gitignore rule.]**

### [MEDIUM] canonical/agents/build-error-resolver.md — "minimal diffs" contradicted by nuclear recovery
Evidence: :10 "get builds passing with minimal changes — no refactoring, no architecture changes" vs :90 `rm -rf node_modules package-lock.json && npm install` (regenerates the whole dependency tree) and :93 `npx eslint . --fix` (repo-wide rewrite).
Fix: delete "Quick Recovery" or require explicit user confirmation for it, and never delete the lockfile.

### [MEDIUM] canonical/skills/wiki-lint.md vs wiki/data-model.md — archive rules disagree
Evidence: wiki-lint.md:12-13 "`updated` older than 180 days with zero inbound links → archive candidate **per the data model's retirement rules**" vs data-model.md:74 "`verified` older than 180 days **and** zero inbound `relates_to` links". The lint cites the data model while using a different field.
Fix: change the lint to use `verified`, matching the data model it cites.

### [MEDIUM] canonical/mcp/filesystem-wiki.json — write access to the whole wiki breaks the wiki's immutability rules
Evidence: args `@modelcontextprotocol/server-filesystem ./wiki` grants read/write on all of `wiki/`. AGENTS.md:45 says `wiki/raw/` is "Never edit. Agents read, never write", and AGENTS.md:39 says "Raw session logs are never edited". `./wiki` is also resolved against the MCP server's cwd, not the repo root. Both tools already have native file access, so the server adds risk and nothing else.
Fix: remove it, or pin an absolute path and make it read-only.

### [MEDIUM] canonical/mcp/*.json — unpinned `npx -y` supply chain, possibly deprecated server, empty token
Evidence: all 5 servers run `npx -y <pkg>` with no version. context7.json pins `@latest`, so every session start can execute newly published code. github.json uses `@modelcontextprotocol/server-github`, which upstream appears to have deprecated in favor of `github/github-mcp-server` (verify before merge), and sets `"GITHUB_PERSONAL_ACCESS_TOKEN": ""`, which may override the user's exported token with an empty string. playwright.json forces `--browser chrome`, which fails if Chrome isn't installed.
Fix: pin exact versions, drop empty env keys (or use `${VAR}` expansion), and replace or drop the github server.

### [MEDIUM] canonical/hooks/failure-capture.json — hook command depends on cwd
Evidence: `"command":"./scripts/sidecar.sh record-failure"` goes through unchanged to .claude/settings.json and .github/hooks/failure-capture.json. If the shell is not at the repo root, the hook fails, so failures are silently not captured.
Fix: emit `"$CLAUDE_PROJECT_DIR"/scripts/sidecar.sh` for Claude, and use the equivalent absolute path for Copilot.

### [MEDIUM] scripts/adapters.py — reinstall wipes user hooks and never removes stale outputs
Evidence: adapters.py:151 `settings["hooks"] = settings_hooks` replaces the entire hooks key in `.claude/settings.json`, so any hook a user added is lost on every `install.sh`. The install functions (:60-142) only write. A renamed or removed canonical skill or agent leaves an orphan in `.claude/` and `.github/` that both tools keep loading.
Fix: merge only adapter-owned hook entries, and delete generated files that have no canonical source (keep a manifest).

### [MEDIUM] canonical/skills/codebase-onboarding.md — can create the CLAUDE.md suppression trap
Evidence: :173 "Generate or update a project-specific CLAUDE.md / AGENTS.md"; :224 "a `CLAUDE.md` / `AGENTS.md` written to the project root". If the agent writes a standalone CLAUDE.md with no `@AGENTS.md` import, that is exactly arm C: the shared AGENTS.md is silently not loaded (P2-claudemd-drop, 2/2). Run in this repo, "enhance existing CLAUDE.md" (:208) also bloats the bridge.
Fix: make AGENTS.md the only generated target, and have CLAUDE.md be `@AGENTS.md` plus annex only.

### [MEDIUM] canonical/agents/doc-updater.md — relies on machinery and a stack that don't exist here
Evidence: :3 "Backs the /update-codemaps and /update-docs commands". `ls .claude/commands .github/prompts` gives "No such file or directory". :23 `npx tsx scripts/codemaps/generate.ts`: `test -f` exits 1 and `scripts/codemaps` doesn't exist. `docs/CODEMAPS/` doesn't exist, and there's no `package.json`/`tsconfig.json`. The whole agent assumes TypeScript and this repo is Python/bash.
Fix: drop the agent, or rewrite it without the TypeScript toolchain and the command references.

### [MEDIUM] .github/muse-instructions.md — the Copilot-only instruction file may never load
Evidence: E1 addendum (evals/results/2026-09-30-E1-partial.md:40-50): an isolated dir containing only this file reports "No instruction sources found". `copilot instruction list` shows only AGENTS.md and CLAUDE.md. tips-copilot.md:22 vs :24 uses `muse-instructions.md` at repo level but `copilot-instructions.md` at user level, which is inconsistent. It's marked "locally UNVERIFIABLE", yet README.md:33 presents it as the Copilot entry point.
Fix: run the authenticated probe before merge. Otherwise rename it to the filename the CLI actually loads, or delete it.

### [LOW] canonical/agents/refactor-cleaner.md — commits on its own
Evidence: :44 "Commit after each batch" and the checklist "Committed with descriptive message". The agent makes commits the user never asked for.
Fix: stage and report instead of committing, and leave commits to the user.

### [LOW] canonical/agents/build-error-resolver.md — hands off to a nonexistent agent
Evidence: :107 "Architecture changes needed → use `architect`". `ls canonical/agents` has `code-architect.md` and no `architect`.
Fix: change it to `code-architect`.

### [LOW] AGENTS.md — `wiki/raw/` is missing
Evidence: AGENTS.md:45 defines `wiki/raw/` as the immutable source layer. `ls wiki/raw` gives "No such file or directory" (wiki/ has data-model.md, index.md, log.md, notes, sessions, telemetry).
Fix: create it with a README, or remove the layer from the schema.

### [LOW] AGENTS.md vs canonical/skills/session-harden.md — session log mutability and log-line format disagree
Evidence: AGENTS.md:39 "Raw session logs are never edited after the fact" vs AGENTS.md:37 "Mark the session file status" and session-harden.md:18 "fill in its `## Outcome` section", which are both edits. AGENTS.md:36 log line = "date, session file, outcome" vs session-harden.md:17 = "timestamp, tool, `session`, session filename, outcome".
Fix: say the turn log is append-only but frontmatter and Outcome are mutable, and define one log-line format in data-model.md.

### [LOW] AGENTS.md §6 — telemetry is promised for both tools but works on one
Evidence: AGENTS.md:1-3 applies §6 "whether you are Claude Code or GitHub Copilot CLI". AGENTS.md:83 says "Hooks capture structured events (… token counts)". adapters.py:127-130 says the Copilot hook is REFUTED on CLI v1.0.89 ("no events fired"), and no hook anywhere captures token counts.
Fix: scope the §6 claims to Claude and drop "token counts" until something captures them.

**Pass 4 count: 3 HIGH, 9 MEDIUM, 5 LOW (17 findings).**

---

## Orchestrator verification (Helm, 2026-09-30)

Spot-checks run independently against disk after the Opus passes; ≥5 required, 8 performed:

| # | Finding | Label | Check |
|---|---------|-------|-------|
| 1 | S12 BLOCKER (treatment was a hand-written CLAUDE.md, not AGENTS.md/wiki; S3 UNVERIFIABLE) | **CONFIRMED** | ledger:36 vs ledger:25; `P2-realcode-prereg.md:172-174` (arm 3 = CLAUDE.md with frozen orientation text); `P2-realcode-ab.md:7-8` (all runs Haiku 4.5) |
| 2 | S12 combined rule registered after NetworkX result | **CONFIRMED** | `git log`: `025dea6` (NetworkX n=8 result) precedes `d85c6e5` (Rich prereg) |
| 3 | S4 Copilot mechanism retracted by its own evidence | **CONFIRMED** | `E4.md:53-87` addendum: "the attribution was wrong"; "S4's Copilot leg changes from REFUTED to PARTIAL-with-mechanism" |
| 4 | S5 "probe inputs −51%" is uncached-only; total input −1.9% | **CONFIRMED** | Transcript envelopes: all-notes 10,421+18,071+42,917 = 71,409; active-only 5,083+9,707+55,229 = 70,019 |
| 5 | S5 corpus-truth score 6/10 → 5/10 (Q4: active "0" vs all-notes "15") | **PARTIALLY VERIFIED** | Both Opus passes independently derived the Q4 discrepancy from the transcripts; the saved envelopes are result-only (255/464 chars), so the full Q&A cannot be re-extracted from the repo — which itself confirms the auditability half of the finding (probes + answer key not on disk) |
| 6 | S6b REFUTED rests on a permission-blocked pilot | **CONFIRMED** | `E6-pilot-copilot-transcript.txt:37-41`: first writes fail "Permission denied and could not request permission from user"; Copilot never rerun under trust |
| 7 | S14 PROVEN includes a port REFUTED as-shipped in both tools | **CONFIRMED** | `P2-port-verification.md:101`: playwright "call REFUTED as-shipped in this sandbox" in both tool columns |
| 8 | Pass 4 HIGH: adapters.py drops `tools_hint`; read-only agents get all tools | **CONFIRMED** | `canonical/agents/planner.md:5` declares `[read, search]`; `adapters.py:79,84` emit name+description only; emitted `.claude/agents/planner.md` has no `tools:` line; 0 of the emitted agent files contain `tools:` |
| 9 | Pass 4 HIGH: failure payloads land in a git-tracked file | **CONFIRMED** | `git ls-files` lists `wiki/telemetry/events.jsonl`; `.gitignore` has no telemetry rule |
| 10 | Pass-1-era S8 item ("no raw body for the default-mode run") | **WRONG (reviewer error, corrected)** | `~/agent-logs/claude/raw-default/` holds an 82,441 B request body; Pass 1A's S8 MINOR (missing prerequisites/caveat in the ledger) stands, the "no artifact" sub-claim does not |

Ledger actions taken on this branch (marked, not deleted): S4 Copilot leg corrected; S5 token/score wording corrected; S6b REFUTED scoped to default permissions with capability reading UNVERIFIABLE; S12 scope correction appended (PROVEN retained for the narrowed claim only); S14 verdict downgraded PROVEN → PARTIAL.

Spend: metered via CLI JSON envelopes — full claims pass $1.4033, S1–S9 claims pass $1.1059, smoke $0.0116, narrative+CLAUDE.md pass $0.6744, setup pass $0.6306 = **$3.8257 total metered** (all envelopes recovered; two arrived in late completion notifications after their harness wrappers reported failure). Model for all passes: `claude-opus-5-5` (Claude Code 2.1.285, `--model opus`, `--bare` + apiKeyHelper).
