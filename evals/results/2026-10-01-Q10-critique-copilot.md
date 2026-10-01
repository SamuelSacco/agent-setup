# Q10 adversarial critique — Copilot critic (verbatim)
Model: claude-opus-5-5, HEAD: 2abc02b1d5f117cfbe486dc202632bb0f280a391
# Hostile review of SamuelSacco/agent-setup (HEAD 2abc02b)

I edited no project files. I ran `install.sh` and `quickstart.sh` in a fresh local clone with a scratch `HOME`. The scratch clone was deleted afterwards.

## Findings

1. **[critical] [stranger/claims]** Location: `canonical/agents/tdd-guide.md`, `canonical/skills/search-first.md`, `canonical/skills/tdd-workflow.md`; `scripts/adapters.py` `fm_block`; ledger S14.
   - Evidence: the Copilot CLI 1.0.90 log for this session (`~/.copilot/logs/process-…-23934.log:29-30`) says: `[ERROR] .github/agents/tdd-guide.agent.md: custom agent markdown frontmatter is malformed: failed to parse YAML frontmatter: mapping values are not allowed in this context at line 2 column 182`. The same error appears for `.claude/agents/tdd-guide.md`.
   - In a live Copilot session started from the repo root, only 7 of 9 skills were exposed (search-first and tdd-workflow missing) and 11 of 12 agents (tdd-guide missing). PyYAML rejects all three emitted frontmatters.
   - Problem: the ledger's "12/12 agents, 8/8 skills in both tools" is false at HEAD. Three capabilities fail to load. The cause is that `fm_block` writes descriptions containing `: ` without quoting them.
   - Fix: quote or YAML-dump frontmatter values in `fm_block`, add a parse check to quickstart, and re-verify S14.

2. **[major] [stranger]** Location: `scripts/quickstart.sh` §3 (structural verify).
   - Evidence: the command `HOME=… PATH=stub:$PATH ./scripts/quickstart.sh --structural-only` printed `ok claude agents: 12/12` … `structural verify: PASS` while tdd-guide is unparseable.
   - Problem: the check counts files. It never parses them, so it certifies broken output.
   - Fix: parse each frontmatter with a YAML parser and fail on error.

3. **[major] [stranger/consistency]** Location: `README.md` and `docs/setup.md:77` ("8/8 skills and 12/12 agents"); `scripts/install.sh:7`; ledger S14.
   - Evidence: `install.sh` prints 9 `skill` lines and then `(structural verification: 8/8 skills, 12/12 agents…)`. Quickstart then prints `ok claude skills: 9/9`.
   - The 9th skill, `self-review`, was added in 7220a9f on 2026-10-01. The evidence for the 8/8 figure is `P2-port-verification.md:9` and `installer-safety.md:50`, both from 2026-09-30.
   - Problem: the count drifted, and the PROVEN evidence predates the current inventory.
   - Fix: derive counts from `canonical/` at runtime, and re-run S14 with all 9 skills.

4. **[major] [stranger]** Location: `scripts/quickstart.sh:52-71`.
   - Evidence: the command `HOME=<scratch> ./scripts/quickstart.sh --structural-only` printed `installing claude via npm into ~/.local (no sudo)...` and then hung until my 60 s timeout (exit 124). With `npm`/`npx` off PATH it printed `FAIL: claude not found and npm unavailable.`
   - Problem: "structural-only" still requires both CLIs and network access, and it silently `npm install -g`s unpinned latest versions. Nothing checks the README's `>= 2.1.277` floor.
   - Fix: skip `ensure_cli` under `--structural-only`, pin or floor-check versions, and call `check-version-guard.sh`.

5. **[major] [missing/security]** Location: `scripts/adapters.py:137-139, 310-358`; `docs/setup.md` §4.
   - Evidence: `install.sh` writes `~/.copilot/mcp-config.json`, which loads in every Copilot session on the machine. It contains `filesystem-wiki` with an absolute clone path, `playwright --browser chrome`, and `"tools": ["*"]` for all 5 servers. The real `~/.copilot/` on this host holds 18 `mcp-config.json.bak-*` files.
   - Problem:
     - setup.md §4 does not disclose the write to HOME.
     - Repo-scoped capabilities leak into every project.
     - With multiple clones, the last install wins.
     - There is no uninstall path and no backup pruning.
   - Fix: document the HOME write, add `--uninstall` and backup rotation, and namespace server names per clone.

6. **[major] [missing/security]** Location: generated MCP config, `github` server.
   - Evidence: `"@modelcontextprotocol/server-github@2025.4.8"` with `"env": {"GITHUB_PERSONAL_ACCESS_TOKEN": ""}`.
   - Problem:
     - That package is the archived reference server, superseded by `github/github-mcp-server`.
     - The hard-coded empty token likely overrides an inherited token. I did not test this.
     - `npx -y` pins versions but not hashes; X6 hash-pinning is a prototype only.
   - Fix: switch to the maintained server, drop the empty env value or pass the variable through, and adopt integrity pinning.

7. **[major] [stranger]** Location: `scripts/quickstart.sh:17-19, 135`.
   - Evidence: the script says the probe answer "exists only in an installed skill's body". The answer (wiki/raw is never edited; complete/partial/abandoned) is also in AGENTS.md §2/§3, which loads natively.
   - Problem: the live probe can pass without any skill being discovered.
   - Fix: use a nonce that appears only in one skill body.

8. **[major] [stranger/consistency]** Location: `scripts/quickstart.sh` §3; `docs/setup.md` Troubleshooting ("MCP server missing → .github/mcp.json").
   - Evidence: quickstart validates `.github/mcp.json` "servers". Per S24, Copilot workspace MCP files never load.
   - Problem: it checks a file Copilot ignores and skips `~/.copilot/mcp-config.json`, the one that matters. The troubleshooting advice points users at a dead file.
   - Fix: verify the user-scope file and correct the troubleshooting row.

9. **[major] [claims]** Location: ledger S6.
   - Evidence: "PROVEN … n=1 task package, boundary … blind scores 10 vs 9, diff 1 = pre-registered ≤1 threshold". The scope is `backend`, TokenBucket, Haiku.
   - Problem: the claim reads "Shared specialist agents behave consistently across both tools". That is general wording on n=1, one agent, one model, sitting exactly at the threshold. `docs/deck.html:38` still says "parity UNVERIFIABLE (S6)", so the ledger and deck disagree.
   - Fix: narrow the wording to "backend agent, one task, Haiku" and reconcile the deck.

10. **[major] [claims]** Location: ledger S1; `deck.html:98`.
    - Evidence: the S1 row says "PROVEN … Claude Code did the same", then its audit note says "Claude leg … permission prompt blocked; discovery inferred from invocation; one skill, Haiku 4.5". `E1-partial.md:37-38` reads "Claude half: UNVERIFIABLE until Claude sign-in completes."
    - Problem: the generic claim ("a canonical skill … BOTH tools") rests on one skill, an incomplete Claude run, and inference. Finding 1 refutes it for 2 of 9 skills.
    - Fix: narrow the claim to `session-harden` and move the verdict to PARTIAL/UNVERIFIABLE for Claude.

11. **[major] [claims]** Location: ledger S3 / X8.
    - Evidence: `X8-e3-wiki-value.md:244` shows A 5/5 vs B 1/5, with tokens 1,083,101 vs 1,836,625. That is −41%, which traces. However, attempts were discarded only in the B arm (T2-B, T3-B, T5-B attempt 1; lines 151-222). The run is Haiku-only and self-run.
    - Problem: asymmetric discards plus contamination incidents weaken the effect. "Token overhead −41%" compares a passing arm against failing arms. The row has an extra column that breaks the table.
    - Fix: state the discard asymmetry in the verdict, re-run B cleanly, and fix the table.

12. **[major] [claims]** Location: ledger S12.
    - Evidence: the ledger's own audit note says the combined rule was registered after the result (025dea6 precedes d85c6e5).
    - Problem: a post-hoc rule cannot yield PROVEN.
    - Fix: downgrade the verdict to UNVERIFIABLE, or re-run under a rule fixed in advance.

13. **[major] [claims]** Location: ledger S25.
    - Evidence: the title covers Claude and Copilot, but PROVEN covers Claude only. The behavior run passed on rerun after the skill was edited to fit the fixture (`S25-self-review-rerun.md`).
    - Problem: the scope shrank, and the evaluator tuned the skill to the test.
    - Fix: split S25 per tool and re-test on a fresh fixture.

14. **[major] [claims]** Location: ledger S21.
    - Evidence: the headline is "PROVEN (emission, structural)". The Evidence column records Copilot enforcement as REFUTED (code-reviewer wrote files via a bash heredoc). The row also still says "CLI not installed".
    - Problem: a REFUTED security-relevant result is buried, and the row is stale.
    - Fix: give it a two-part verdict and remove the stale text.

15. **[minor] [claims]** Location: ledger S15, S2.
    - Evidence:
      - S15: PROVEN for code-reviewer only; 3 other agents REFUTED.
      - S2: one direction (Copilot→Claude), n=1, recall-only. The critique says the baseline was recoverable from git (`claude-critique-2026-09-30.md:44`).
    - Problem: the headlines are broader than the evidence.
    - Fix: scope each headline to what was tested.

16. **[major] [claims]** Location: ledger, whole document.
    - Evidence: audits are labeled "claude-opus critique" and "copilot critique". The same agents that ran the experiments graded them.
    - Problem: the evidence is largely self-graded. No human or third-party replication is cited for any PROVEN row.
    - Fix: mark self-audited rows as such and get at least one independent re-run of the headline claims.

17. **[minor] [claims/consistency]** Location: ledger S4, S5, S14; S12 audit note; S19.
    - Evidence:
      - The verdict "PARTIAL" is outside the declared PROVEN/REFUTED/UNVERIFIABLE set.
      - S12 says "S3 remains … UNVERIFIABLE", but S3 is now PROVEN.
      - S19 keeps the retracted "no hook loader in installed CLI" mechanism.
    - Problem: the ledger contradicts itself.
    - Fix: either define PARTIAL or split those rows, and update the cross-references.

18. **[minor] [consistency]** Location: ledger table structure.
    - Evidence:
      - The S23 row has no separator before `**PROVEN**`.
      - The S24 row has no Evidence column.
      - Blank lines cut S18 and S27 out of the rendered table.
      - Rows are out of order (S20, S18, S21).
    - Problem: the table renders broken on GitHub.
    - Fix: lint the table in CI.

19. **[major] [overstatement]** Location: `README.md:7`; `deck.html:38, 68-70`.
    - Evidence: README: "Clone it, run the installer, and both tools behave the same." Deck: "Launch copilot → same skill, same behavior."
    - Problem: S4 (Copilot failure capture 0/5), S21 (Copilot enforcement REFUTED), S15, S24 (different MCP scopes), and finding 1 all contradict this.
    - Fix: delete the sentence, or replace it with the scoped verdicts.

20. **[major] [overstatement]** Location: `deck.html:101, 138`.
    - Evidence: "E5: orientation tokens −38% … nothing active-scope lost". The audit correction in ledger S5 says total input fell ~2% (71,409 → 70,019) and that −51%/−38% count uncached input only.
    - Problem: the deck repeats a number its own audit disowned.
    - Fix: use the total-input figure, or label the −38% as "uncached input only".

21. **[minor] [overstatement/consistency]** Location: `deck.html:66, 100, 131, 139`.
    - Evidence:
      - Line 66: "install.sh does not yet emit" `~/.copilot/mcp-config.json`, but it does.
      - Lines 100/131: "E3 … UNVERIFIABLE / remains unrun", but S3 is PROVEN via X8.
      - Line 139: "no cleanup skill exists yet … self-review … not merged", but `canonical/skills/self-review.md` is present.
      - Line 5: "SessionEnd … in Copilot … 3/3", while `AGENTS.md` §8 says the Copilot sessionEnd hook is UNVERIFIABLE.
    - Problem: the deck is stale on four counts and contradicts AGENTS.md.
    - Fix: regenerate the deck from the ledger.

22. **[minor] [overstatement]** Location: `deck.html:135`.
    - Evidence: "Keep the tool surface ≤ ~35 tools per agent", followed in the same paragraph by "The ~35-tool threshold is UNVERIFIABLE folklore".
    - Problem: an unverified threshold is presented as a rule. S26 explicitly did not test it.
    - Fix: drop the number, or present it as an untested heuristic.

23. **[minor] [consistency]** Location: `README.md:89`; `scripts/adapters.py:9, 17, 353`.
    - Evidence:
      - The README pins "Copilot CLI 1.0.89", but the installed CLI is 1.0.90 (X11).
      - adapters.py cites "ledger S18" for SessionEnd; the row is S19.
      - The docstring lists agent frontmatter `model`, which is never emitted, so `model_hint` is silently dropped.
    - Problem: version references and code comments have drifted from the ledger.
    - Fix: update the version and the citation; either emit `model` or remove it from the docstring.

24. **[minor] [missing]** Location: `canonical/hooks/failure-capture`; install output `hook failure-capture -> claude + copilot`.
    - Evidence: S4 records 0/5 failures captured on Copilot.
    - Problem: a hook known not to work on Copilot is installed there without any warning.
    - Fix: skip it on Copilot, or print a warning at install time.

25. **[minor] [stranger]** Location: `README.md` and `docs/setup.md` §2/§5.
    - Evidence:
      - `copilot login` has no verification step.
      - §5 expects the agent to create a session file, which is unverified.
      - Node/npx are needed for all 5 MCP servers but quickstart only WARNs about them.
      - `install.sh` ends with "Discovery by each tool is UNVERIFIED", while the ledger says PROVEN.
    - Problem: there are undocumented prerequisites, and the tool's own output contradicts the ledger.
    - Fix: list Node ≥ X as a hard prerequisite, add auth checks, and align the wording.

26. **[minor] [missing]** Location: repo-wide.
    - Evidence: there is no CI, no cost cap enforcement, and no upgrade or drift procedure. S16 overshot its cap ($4.63 vs ~$4). The repo root has stray untracked `raw-copilot.txt` and `raw-copilot.stderr.txt`.
    - Problem: the maintenance burden falls on manual agent sessions.
    - Fix: add a CI job running install, a YAML parse check, the ledger table lint, and the version guard.

I found no missing evidence files: every `evals/results/…` path cited in the ledger resolves. The X8 headline numbers trace to their source; the problems with them are method problems.

## Verdict

1. I would not trust the PROVEN column as written. Most rows are true only for n=1, Haiku, one agent or skill, and self-graded.
2. HEAD has a live, reproducible defect that refutes S14 and the README counts: 3 of 21 capabilities fail to load in Copilot because of malformed YAML.
3. Quickstart cannot catch that defect. It counts files, checks an MCP file Copilot ignores, and its probe is answerable from AGENTS.md.
4. The deck and README make broader claims than the ledger, and in several places stale ones (E3, E5, MCP emission, self-review).
5. Credit is due for recording REFUTED results and audit notes, but post-hoc rules, asymmetric discards, and self-audit mean the headline verdicts need independent re-runs before anyone relies on them.

