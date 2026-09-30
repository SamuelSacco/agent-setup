# Path forward — agentic-coding presentation

Written 2026-09-30 ~01:40 EDT. Read-only review; nothing here was executed.
Anchor facts: repo at `736c93f`, clean tree. Ledger verdicts: S1 PROVEN,
S2 PROVEN (5/5, clean control), S4 PARTIAL (Claude 5/5, Copilot v1.0.89
REFUTED), S5 PARTIAL (token axis 38%), S7 PROVEN (BYOK). S3, S6 UNVERIFIABLE.
Deck updated through E2/E4/BYOK; two artifact builds (deck pptx, guide PDF)
were dispatched pre-pause and then interrupted — treat as **not built**;
confirm via `artifact.status` before re-creating.

## 0. Deadline and the date contradiction

- Memory: build frozen **2:00 PM Oct 1**, grill **2:00–4:00 PM Oct 1**,
  org presentation **4:00 PM Oct 1**. Work-team group page also says Oct 1.
- The pre-compaction summary said Sept 30. **Contradiction flagged.**
  Repo itself states no presentation date (grep: only "researched
  2026-09-30"), so nothing in-repo to fix.
- Plan assumes **Oct 1**. Cost if wrong (really Sept 30): §1 items 1, 2, 6
  and §5 still fit before 2 PM today; E6/E3 get cut (§3). Samuel to
  confirm the date at wake-up — one line, no meeting.

## 1. Remaining work, dependency order (overnight, while Samuel sleeps)

Wall-clock estimates are agent-work time; items 2–4 parallelize.

1. **Deck factual pass** — 20–30 min. **Blocking; do first.**
   - `docs/deck.html:73` cites `canonical/mcp/coralogix.json`. No such
     file exists (only `canonical/mcp/filesystem-wiki.json`). Replace the
     example with the real file.
   - `docs/deck.html:190` presents GitLab CLI / Coralogix / Mongo /
     Okteto / Atlassian / Chrome DevTools / CodeRabbit / Figma as joining
     "through the same door." None have canonical files today. Reword to
     future adapter slots, or the slide asserts what we refute elsewhere.
   - Re-check every verdict tag against `docs/claims-ledger.md`; kill any
     "live today" / "UNVERIFIABLE → live" remnant.
2. **E5 quality axis** — 30–45 min, ~$0.06–0.12 (anchors below). S5 is the
   cheapest open verdict: 10 E2-style probes under active-only vs all-notes
   on the seeded wiki; score; flip S5 to PROVEN or REFUTED either way.
3. **E6 pilot, then decision** — pilot 20–30 min; full matrix +60–90 min.
   Gate in §2. Runs only under the pre-registered cap, actuals logged.
4. **E3 reduced** — 60–90 min, ~$0.35–0.80. Optional (§2). If run at
   3 tasks instead of the pre-registered 5, log the deviation in the
   results file; a silent design change voids the verdict.
5. **Grill-prep refresh** — 20 min, after 1–3 so the answers cite final
   verdicts. Add the cold-explain checklist (§4) to `docs/grill-prep.md`.
6. **Artifact builds** — deck (pptx) + follow-along guide (PDF) from the
   corrected `docs/`. 30–60 min elapsed. Guide falls back to the `docs/*.md`
   set if the PDF builder fails; do not let packaging block §5.
7. **Final commit + push** — 10 min. Terse message: what changed and why.
   Then freeze. No eval runs after freeze; evidence corrections only.

Morning (Samuel awake, before 2 PM):

8. **Stage-machine smoke test** — 15 min, Samuel's hands, guided by a
   5-line checklist. On the actual present machine: `claude` one prompt,
   `copilot` one prompt, `./scripts/install.sh` on a fresh clone, open
   `wiki/telemetry/events.jsonl`. Everything proven so far ran in Helm's
   sandbox; stage auth (Claude OAuth, Copilot login) is unverified there.
9. **Gmail delivery** — deck + guide to Samuel's Gmail after his morning
   review, per send-confirmation rules. Not fired silently overnight.
10. **Grill session 2:00–4:00 PM** (§4), presentation 4:00 PM.
11. **Leave `appacademy`** — after the presentation completes. Not before,
    not during. He is a member, not owner; entitlement is personal and
    unaffected.

## 2. E6 go/no-go and the spend estimate

Measured anchors (Claude, Haiku, stored key): bounded session $0.026–0.043
at 4–8 turns (E1/E2/E4 result files). Copilot BYOK overhead: ~14.5k input
tokens vs ~1.9k for a one-word reply — harness tax is real but task content
dominates on real work; assume Copilot run = 1.5–3× the Claude run.

Method — **pilot extrapolation, never a guess**:

1. Pre-register a hard cap in the results file *before* running: **$2.00
   total** for E6, $3.00 total for all overnight eval spend. Log actuals
   per run (`evals/results/` + a spend log). Hit cap → stop, report.
2. Pilot: `backend` agent, one bounded task, both tools (2 runs).
   Projected = pilot pair cost × remaining pairs × 1.5 headroom.
3. **GO** full matrix (3 agents, matched tasks, both tools) iff projected
   ≤ $2.00, overnight slack ≥ 2 h after item 1–2, and BYOK auth stable.
   **NO-GO** otherwise: S6 stays UNVERIFIABLE. The deck already shows it
   that way; the talk does not depend on E6.
4. Blind scoring is part of the claim: outputs stripped of tool labels,
   scored by a fresh-context scorer. If scoring can't be blind, the best
   attainable verdict is "PARTIAL (unblinded)" — say so, don't upgrade.

**E3/E5 verdict:** E5 quality axis — yes, do it (item 2: cheapest verdict
flip available). E3 full — no. E3 reduced — only if items 1–2 and the E6
decision leave slack; its question ("does the wiki help?") is partially
covered by E2's clean control, and an honest UNVERIFIABLE with the
threshold printed beats a rushed PASS the night before.

## 3. Cut order if time runs short

Cut in this order; never cut item 1, 2, 6, 7, 8:

1. E3 reduced (S3 stays UNVERIFIABLE — honest, already on the slide).
2. E6 full matrix → pilot only, reported as pilot, S6 UNVERIFIABLE.
3. Demo Act 4 (rubber duck / `/advisor` live) — tips slides carry it.
4. Guide PDF → ship `docs/*.md` as the follow-along.

## 4. Grill checklist — Samuel explains these cold, in his own words

- Why `CLAUDE.md` starts with `@AGENTS.md` (native AGENTS.md read only
  since Claude Code v2.1.277, and only when no CLAUDE.md exists).
- canonical → adapter → `install.sh`; never edit adapter output by hand.
- Session lifecycle: orient → log → harden; the wiki is the memory,
  not the model.
- E2's trap answer: the separator decision lives in the session record,
  in **no** wiki note — and the no-wiki baseline invented nothing.
- E4 split verdict: `PostToolUse` fires on success; failures live on
  `PostToolUseFailure`. Copilot v1.0.89: binary has no hook loader —
  "refuted on this build," never "Copilot has no hooks."
- BYOK: same Anthropic key and model in both harnesses; proof is the
  footer — tokens metered, no AI Credits line. Harness is the variable.
- His Copilot entitlement: personal `free_limited_copilot`, 200 requests,
  overage off — and `appacademy` supplies nothing.
- Why JSONL/SQLite, not Postgres (single writer, low volume; Postgres
  earns its place at concurrent writers / cross-machine queries).
- `/advisor` cost shape: cheaper than Opus-only, not token-neutral.
- What is still UNVERIFIABLE (S3, S6) and the kill criteria. Naming the
  gaps unprompted is the credibility move.

## 5. Never fake

- A live result (backup pack exists precisely so a dead live beat becomes
  a narrated record, labeled as such).
- A verdict: UNVERIFIABLE stays until the pre-registered test runs.
- "OTEL": the sidecar is JSONL shell telemetry, not OpenTelemetry.
- Copilot hooks (refuted on v1.0.89), plugin translation
  (`canonical/plugins/` is empty), project-MCP enumeration (did not
  appear in `copilot mcp list`), premium/Astra access (unverifiable).
- Numbers: Claude dollars and Copilot AI Credits are different units;
  credits are not verified dollars. Samuel's own credit purchase
  amount/receipt was never observed — don't cite one.
- The org toolchain (GitLab, Coralogix, Figma, …) as implemented. Slots.

## Summary

Fix the two deck inaccuracies, close E5's quality axis for ~a dime, gate
E6 behind a measured pilot and a $2 pre-registered cap, refresh grill prep
around ten cold-explain lines, rebuild the two artifacts, commit, freeze —
with Samuel's only morning jobs being a 15-minute stage-machine smoke test
and the Gmail send approval. The single biggest risk is environment
transfer: every proof so far ran in Helm's sandbox, so if the stage
machine's Claude/Copilot auth differs, the live demo fails in the first
minute — the smoke test (item 8) plus the text backup pack are the whole
mitigation, and skipping the smoke test to "save time" is the one cut that
must never happen.
