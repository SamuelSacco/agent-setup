# Claims audit — Phase 2 packet, addendum, and ledger

**Bottom line:** the strongest evidence is in the disk-graded, task-specific experiments; the weakest part is the conversion of narrow results into broad “PROVEN” statements about efficacy, parity, and turnkey adoption. The reports often disclose their own limits, but headlines and ledger verdicts do not always preserve those limits. The most material issue is not fabricated evidence: it is scope inflation, plus one stale ledger rationale that contradicts its own corrected result.

## Findings, ordered by severity

### High — S12's “PROVEN” is valid only as a narrow protocol result, not as a general orientation effect

The NetworkX numbers are real within the described experiment: base 6/8 versus orientation 8/8, with two discordant task pairs. But both deciding pairs are from one codebase, and the second codebase (Rich) is 3/4 versus 3/4 with no discordant pair. The R2 “win” is especially weak as evidence of a substantive behavioral improvement: the base arm raised the same exception type but used “No nodes in graph,” while the fix test expected text matching “null graph.” The report records that this pair turns on message wording, not the exception or behavior class. See `tree/evals/results/2026-09-30-P2-realcode-ab.md:130-198,300-350`.

The combined “PROVEN” rule for NetworkX plus Rich was specified before the Rich runs, but after the original NetworkX and replication results were already known (`...P2-realcode-ab.md:300-305`). It is a pre-registered extension rule, not an independent preregistration of the entire 12-task claim. A pooled 11/12 versus 9/12 tally disguises that all wins came from NetworkX; Rich contributed no positive pair. The ledger does disclose this (`tree/docs/claims-ledger.md:36`), and the result says the same (`...P2-realcode-ab.md:343-350`), but the addendum headline still leads with “11/12 vs base 9/12 across two codebases” (`tree/docs/phase2-addendum-2026-09-30.md:7-21`). The packet's safer proposed stage wording—“NetworkX, Haiku 4.5, our orientation protocol”—is the defensible scope (`tree/docs/phase2-packet-2026-09-30.md:110-119`).

**Verdict check:** PROVEN is reproducible under the report's chosen operational threshold; it does not establish a general causal effect, likely effect size, or cross-codebase replication. For the broad S12 wording, label **PARTIAL** (or retain PROVEN only with an explicit NetworkX/Haiku/protocol scope). Sample is 12 paired tasks, but effective positive evidence is two discordances from a single project, one resting on assertion text.

### High — “one canonical setup serves both tools” is a source-of-truth claim, not demonstrated parity or turnkey reliability

The packet says “all live-invoked, both tools” (`tree/docs/phase2-packet-2026-09-30.md:46-79`), but the results establish a narrower claim: selected capabilities can be discovered and invoked in tested configurations. The install matrix found an actual Copilot MCP adapter defect, and the subsequent port report still records trust gating and cold-cache startup failures. It also records Playwright failing as shipped in the root sandbox and passing only after adding `--no-sandbox` in a scratch config; use on a normal non-root developer machine remains UNVERIFIABLE. Authenticated GitHub operations are likewise untested (`tree/evals/results/2026-09-30-P2-port-verification.md:93-128`). The failure-capture hook is not behaviorally equivalent: Claude records induced failures, while Copilot's failure event does not identify shell exits (`...2026-09-30-P2-install-matrix.md:162-190`; `...2026-09-30-E4.md:53-87`).

The report itself says the 8 skill probes were “load-and-stop,” proving discovery and invocation, not workflow completion; agent marker probes prove a marker task, not usefulness or quality (`...P2-port-verification.md:73-90,158-163`). S6 remains UNVERIFIABLE, as it should (`tree/docs/claims-ledger.md:28`). Thus “canonical definitions emitted to both tools” is supported; “one setup behaves consistently across both” is not. The packet does list several caveats, but its summary label compresses them into a success state. Do not describe this as behavioral parity.

**Verdict check:** S14's literal “19 ports ... discoverable and invocable in BOTH tools” is too broad for PROVEN when at least one as-shipped MCP path is only PARTIAL/REFUTED in the tested environment and non-root operation was not tested (`tree/docs/claims-ledger.md:38`; port report lines 93-112). Keep per-surface verdicts; overall bundle claim should be **PARTIAL**. S15 is correctly narrowed to one agent and explicitly leaves the other 11 UNVERIFIABLE (`claims-ledger.md:39`).

### High — the primary evidence is not fully auditable from the repository

The Phase 2 packet opens with “Everything below is measured” and says verdicts are disk-derived (`tree/docs/phase2-packet-2026-09-30.md:1-6`). Yet several critical result reports send the reader to runner code, per-run outputs, and ledgers under `~/workspace/p2/...`, rather than storing those artifacts with the result. The real-code report locates its run artifacts outside the repository (`tree/evals/results/2026-09-30-P2-realcode-ab.md:120-128,204-206,352-354`); Copilot and port-verification reports do likewise (`...P2-copilot-ab.md:75-82`; `...P2-port-verification.md:139-163`). Some E-series transcripts are checked in, but that does not make the raw evidence for every headline, cost, diff, and disk grade inspectable here.

The addendum's three-review “verification stack” and instruction-debt counts also cite reports in `~/workspace/`, not repository artifacts (`tree/docs/phase2-addendum-2026-09-30.md:51-87`). In this audit, those secondary assertions—e.g. “4/4 headline claim groups survive,” “ZERO packet claims contradicted,” and the 2,796-line/12-pattern audit—cannot be independently checked against their underlying materials. That is not evidence they are false; it is a provenance/reproducibility gap. “Disk-derived” describes the claimed method, not the durable evidence available to a reviewer.

### Medium — “specialist agents do not pay” generalizes one agent and four tasks

The packet's headline says “Specialist agents do not pay on real code” (`tree/docs/phase2-packet-2026-09-30.md:10-18`). The cited A/B tested one specialist (`backend`) on four NetworkX tasks. It had the same 3/4 solve count as base, no discordant pair, +55% turns, and +8.5% cost (`tree/evals/results/2026-09-30-P2-realcode-ab.md:50-64`). This supports “this backend-agent treatment did not improve this four-task sample”; it does not support a class-wide claim about specialist agents, other domains, or other agents. The ledger's S11 UNVERIFIABLE label is better calibrated than the packet headline (`tree/docs/claims-ledger.md:35`).

**Verdict check:** S11 UNVERIFIABLE is supported. Replace the packet headline with the tested scope; do not promote a negative four-task result into a universal verdict.

### Medium — S2 proves one transfer direction in one session, not tool-agnostic continuity generally

The continuity test transferred one Copilot-authored session record to cold Claude, which answered 5/5 probes; the wiki-removed control answered “not recorded” to all five (`tree/evals/results/2026-09-30-E2.md:5-42`). That is good evidence for this direction and artifact. It does not test Claude-to-Copilot, repeated sessions, conflicts between logs/wiki, or whether arbitrary work remains continuable. The ledger turns that single directional test into “a session in tool A is continuable by tool B” without preserving the direction restriction (`tree/docs/claims-ledger.md:24`).

**Verdict check:** PROVEN for the tested Copilot→Claude record/probe, not for bidirectional or general cross-tool continuity. The report has an honest description; the ledger claim is broader than its cited sample.

### Medium — adoption and “drop this in” language outruns the tested onboarding

The packet labels this section “Adoption (‘drop this in’)” and reports a quickstart prototype plus a fresh simulation (`tree/docs/phase2-packet-2026-09-30.md:81-93`). The same packet says the repo is private—a hard gate for a stranger—and lists missing clone/install/prerequisite instructions and an install script that dirties 32 paths. It also says stage-machine auth is UNVERIFIED and proposes only a 15-minute smoke test (`...phase2-packet-2026-09-30.md:110-119`). The addendum's run-eval proof also used an existing clone and venv; auto-clone and bootstrap are implemented but explicitly unexercised (`tree/docs/phase2-addendum-2026-09-30.md:38-47`).

These facts are candidly disclosed, but “drop this in” reads like an adoption conclusion when the evidence is a prototype/simulation, no external-user install, and no stage-machine auth test. Keep the measured timing, label adoption **UNVERIFIED**, and distinguish “prototype runs in this environment” from “a stranger can adopt it.”

### Medium — S4's ledger rationale is stale and materially wrong

The ledger says Copilot v1.0.89 has “no hook loader” and gives 0/5 (`tree/docs/claims-ledger.md:26`). The cited E4 file preserves that initial diagnosis but explicitly corrects it later: hooks exist, are trust-gated, and fire when trusted; `postToolUseFailure` does not discriminate a shell command's nonzero exit because the shell tool reports success at the tool layer (`tree/evals/results/2026-09-30-E4.md:53-87`). The install matrix repeats the corrected practical limit (`...P2-install-matrix.md:32,190,264-265`). The claim's overall PARTIAL verdict is plausible, but its ledger summary leaves readers with a superseded explanation, not merely an omitted nuance.

**Verdict check:** PARTIAL is appropriate for the shared failure-capture claim; the “no hook loader” premise is **REFUTED by the same cited result's addendum**. The packet's narrower note that Copilot's shell gap is empirical is more accurate.

### Low — S8's “past the 60KB cap” assertion is not demonstrated by the cited run

The ledger says bodies are size-complete past the 60KB cap (`tree/docs/claims-ledger.md:32`). The instrumentation report says the request file was 5,417 bytes, names a response file without reporting its size, then asserts size completeness beyond 60KB and notes thinking text is redacted (`tree/evals/results/2026-09-30-otel-instrumentation.md:17-22`). On the evidence shown in that result, the live probe demonstrates that files were written and content was captured, but not that any captured body exceeded 60KB or that the over-cap behavior was exercised. The redaction caveat is correctly retained; the cap claim needs the actual body size and a demonstrated over-cap case, or narrower wording.

### Low — ledger “PROVEN” is not consistently tied to the stated evidence standard

The ledger's C1 and C2 rows are labeled PROVEN but cite research notes, not an eval result or a live run (`tree/docs/claims-ledger.md:14-16`). That may establish that the features are documented, but the workspace's own instruction says PROVEN means “we ran it.” C4 explicitly says “PROVEN (docs),” a different evidence class from the ledger's live-test verdict vocabulary (`claims-ledger.md:17`). Keep documentation-confirmed claims distinct from behavior observed in a run; otherwise PROVEN conflates “vendor documents this” with “tested in this version/configuration.”

## Hardest expert Q&A on the weakest claims

| Claim | Hardest question | Does the repo contain an honest answer? |
|---|---|---|
| S12 orientation benefit | “Why call this PROVEN across codebases when Rich has zero discordant pairs and both positive pairs are from NetworkX—one hinging on exact exception wording?” | **Yes, in the results and ledger:** they state Rich is UNVERIFIABLE, both pairs are NetworkX's, and disclose the R2 wording issue (`...P2-realcode-ab.md:192-198,337-350`; `claims-ledger.md:36`). **But** the addendum headline's 11/12 pooled framing still invites a broader takeaway. |
| Shared canonical setup / S14 | “What works from a clean, cold, ordinary developer install without trust switches, cache warming, sandbox flags, or auth setup?” | **Partly.** Trust gating, cold-cache failures, Playwright's scratch-only `--no-sandbox` success, and untested authenticated GitHub operations are reported (`...P2-port-verification.md:93-128`). There is no clean non-root, cold-cache end-to-end test supporting a blanket answer. |
| S2 continuity | “Has Claude→Copilot continuity been tested, or only Copilot→Claude?” | **Yes:** the E2 method identifies Copilot as tool A and Claude as tool B; the reverse direction is not tested (`...E2.md:5-18`). The ledger should say so. |
| “Drop this in” adoption | “Can an unaffiliated stranger clone and set this up, authenticate both tools, and run the demo without help?” | **Yes, candidly no:** repo privacy is a hard gate; the quickstart is a prototype/simulation; stage auth remains unverified (`...phase2-packet-2026-09-30.md:81-93,110-119`). |
| S17 eval runner | “Did the proof exercise the promised automatic clone and venv bootstrap from a packaged task?” | **Yes:** the addendum says it used `--source` and an existing venv; defaults were not exercised (`...phase2-addendum-2026-09-30.md:38-47`). The narrowly stated disk-grade path is proven; turnkey bootstrap is not. |

## Evidence-discipline rating: 6/10

The score is held up by concrete good practices: pre-registration for the A/B work, oracle validation, fresh run trees, evaluator-side disk grading rather than self-report, negative controls, explicit cost overruns, and corrections retained in result addenda. The NetworkX/Rich report is unusually clear about the null result and its exception-message caveat. Those choices make the numerical claims inspectable enough to challenge.

The deduction is for claim calibration and evidence custody. Small, task-selected samples are repeatedly summarized with broad “does/pay/proven” language; a null second codebase is pooled into a headline whose positives all come from the first; the S14 bundle label stays PROVEN despite an as-shipped partial; S4's ledger repeats a superseded causal explanation; and the S8 over-cap statement is not evidenced by the file sizes reported. Finally, important raw runs and review reports are outside the tree, so the repository preserves many conclusions better than it preserves the underlying evidence. The result is strong experimental hygiene at the run level, but inconsistent discipline when converting experiments into public claims.
