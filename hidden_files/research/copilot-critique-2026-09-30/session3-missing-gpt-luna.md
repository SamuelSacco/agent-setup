# Adversarial adoption review: what is missing

**Bottom line:** this is a useful, unusually evidence-conscious prototype, not a team-ready agent platform. It demonstrates that some canonical capabilities can be rendered and invoked in both CLIs; it does not yet establish safe, repeatable, supportable operation across a team. The gaps below are ordered by likely consequence, not by how easy they are to fix.

## 1. High — Runtime supply-chain trust is effectively “trust latest”

MCP definitions invoke packages through `npx -y` without a version pin: `canonical/mcp/context7.json`, `filesystem-wiki.json`, `github.json`, `playwright.json`, and `sequential-thinking.json`. For example, Context7 explicitly uses `@upstash/context7-mcp@latest`; the other package specs are also unversioned. `scripts/adapters.py` copies these commands and arguments into tool configuration without a lockfile, digest, signature check, allowlist, or provenance validation. A cache miss or upstream package change therefore turns normal agent startup into execution of whatever code the registry currently serves, under the developer’s local account and whatever ambient credentials/network access the tool has.

There is some provenance work: several ECC-derived agent and skill files carry source/license attribution comments (for example `canonical/skills/verification-loop.md` and `canonical/agents/code-reviewer.md`), and `canonical/skills/search-first.md` describes a review rubric. That is not a supply-chain control. The tree has no pinned upstream commit per imported artifact, central third-party inventory/NOTICE, automated license or vulnerability checks, review gate for updates, or reproducible dependency lock. Markdown skills and agents are executable instructions in practice, but imported prompt content has no repeatable security review either. **This is the single gap most likely to cause a real incident:** a mutable dependency can change behavior without a canonical source change or meaningful review, while being loaded into a privileged agent session.

## 2. High — The installer can destroy local configuration and has no rollback

`scripts/install.sh` simply runs `scripts/adapters.py`; it has no dry-run, backup, transaction, or rollback path. The adapter writes generated files directly. More seriously, `install_hooks()` reads `.claude/settings.json` but replaces its entire `hooks` object with `settings["hooks"] = settings_hooks`; existing user hooks are lost. If the settings JSON is malformed, the `JSONDecodeError` handler silently resets it to `{}` and then writes only the generated hooks. `install_mcp()` overwrites root `.mcp.json` and `.github/mcp.json` wholesale. A failed run partway through can also leave a mixed old/new installation.

The README calls the capability files generated and tells users to rerun the installer (`README.md`, “Principles”; `AGENTS.md`, §4), but nothing stages changes, preserves user-owned entries, reports destructive changes, or retains the last-known-good output. There is no documented uninstall or restore procedure. This is an adoption blocker for developers who already have tool configuration and a credible source of configuration loss.

## 3. High — Sensitive telemetry has no operational data policy

The project knows the risk: `docs/feedback-loop.md` says telemetry can contain prompts and code and advises redacting excerpts before sharing. It also documents Claude raw API-body capture and Copilot full-message capture; `docs/claims-ledger.md` S8–S9 records that these modes were live-tested. Yet there is no stated default-off policy, retention/deletion procedure, access-control or encryption requirement, redaction pipeline, consent boundary, or rule preventing these files from being committed or uploaded. `wiki/telemetry/events.jsonl` exists in the tree, while `.gitignore` only excludes eval scratch directories.

This leaves teams to infer whether session logs, commands, code, prompts, system instructions, and tool definitions are safe to retain in a shared repository. “Local disk” is not a governance boundary when the workspace is cloned, backed up, or pushed. The absence is particularly consequential because telemetry is presented as the audit trail and raw message capture is an advertised capability.

## 4. High — The packaged eval runner is not an isolation boundary

`scripts/run_eval.py` clones task source repositories, extracts a commit into a scratch directory, then runs a coding agent there. Its Copilot arm sets `COPILOT_ALLOW_ALL="true"` (line 175); its Claude arm grants `Bash` and write tools (lines 143–144). The scratch directory is not a container or sandbox: the process still runs as the invoking user, with the host’s network and ambient credentials. The runner’s `git archive` baseline and disk-based grading are good controls against the agent seeing the future fix, but they do not constrain what code or a malicious task prompt can do to the host.

`docs/feedback-loop.md` describes the runner’s grading model and one proof run, but no isolation, credential scrubbing, network policy, or trusted-task review requirement. For a tool intended to evaluate agents against externally sourced code, “fresh tree” is reproducibility, not containment.

## 5. High — No continuous verification of the setup itself

There is meaningful evaluation material: `evals/tasks/`, `evals/tasks-packaged/`, fixtures, and dated results; `scripts/run-eval.sh` can disk-grade a packaged run. The claims ledger is also commendably candid: it records Copilot failure capture as REFUTED (S4), a Copilot agent pilot that claimed success without writing files (S6b), and other partial or unverifiable results. That is valuable research practice.

It is not a setup test suite or release gate. The tree has no CI workflow, conventional tests for `scripts/adapters.py`/`install.sh`, schema or generated-output checks, install/uninstall smoke test, or regression test for preserving existing tool configuration. `docs/feedback-loop.md` explicitly says there is no scheduler or CI wiring and that evals and ledger updates are agent-run/manual. `docs/setup.md` likewise asks adopters to run E1, E4, and E2 manually. There is no automatic check that a canonical change still renders valid configurations for both tools, that stale generated files are removed safely, or that the instructions and file inventory remain consistent.

Also, test coverage is narrow by the project’s own evidence: the packaged runner ships with one task package (`docs/feedback-loop.md`); E5 used a synthetic wiki and its broad quality claim was refuted (`docs/claims-ledger.md`, S5); Copilot orientation is explicitly UNVERIFIABLE at the stated budget (S16). The ledger’s honesty makes these limitations visible; it does not make them release gates.

## 6. Medium-high — No release, compatibility, or rollback discipline

The delivered structure has no visible version manifest, release notes/changelog, supported tool-version matrix, tagged artifact definition, or compatibility policy. Setup instructs users to install and authenticate the current Claude Code and Copilot CLIs (`docs/setup.md`), but does not pin or qualify versions. All live evidence in `docs/claims-ledger.md` is dated 2026-09-30 and includes version-specific behavior (for example Copilot CLI v1.0.89 in S4). There is no process to map those results to a released setup version or to know whether an update remains compatible.

The mutable `@latest` MCP dependencies make this worse: a repository revision does not uniquely identify the software actually loaded. `docs/feedback-loop.md` gives a manual “edit canonical, reinstall, rerun eval” loop, but no staged rollout, approval, release promotion, artifact checksum, canary, previous-version retention, or one-command rollback. Serious teams need to know what is deployed, what changed, and how to return to a known-good configuration.

## 7. Medium-high — Shared use is assumed, not engineered

The project promises sessions shared across tools (`README.md`, Quick start; `AGENTS.md`, §6), but the lifecycle is agent-run and depends on each session creating and hardening the right files (`AGENTS.md`, §§2–3; `docs/feedback-loop.md`, §2). Session names have minute-level timestamps plus tool and slug (`AGENTS.md`, §2), with no collision handling. Notes, index, and append-only log are ordinary shared files with no locking, merge strategy, or conflict recovery.

The telemetry implementation explicitly describes itself as “single-writer” and says multiple concurrent writers are a reason to graduate from flat files (`scripts/sidecar.sh`, comments at the top). That is an architectural caveat, not a multi-user solution. There is no per-user workspace model, role/access policy, synchronized state service, concurrent-writer test, or documented conflict procedure. E2 demonstrates a controlled cross-tool continuation probe; it does not establish concurrent team operation. Two users or agents hardening sessions at once can race on index/notes, collide on names, and create ambiguous audit history.

## 8. Medium — Cost governance is advice and retrospective accounting

`AGENTS.md` says token budgets matter and asks agents to state the cost of a large operation (§7). `docs/feedback-loop.md` records cost after runs and documents an estimate for Copilot. Neither is enforcement: there are no per-run or team-wide budgets, preflight estimates with approval thresholds, hard stop, rate limit, alerts, or controls over expensive model/tool selection. `docs/claims-ledger.md` S16 reports that the Copilot experiment spent $4.63 against an approximately $4 cap before the remaining pairs were stopped. Cost measurement is present; preventing or reliably containing spend is not.

## 9. Medium — Failure handling stops at recording, not recovery

The failure capture work is a useful start, but it is knowingly incomplete: `docs/claims-ledger.md` S4 says Claude capture is proven while Copilot capture is refuted on the tested CLI; `docs/feedback-loop.md` says the Copilot payload-parsing adapter is identified but not built. Session creation, hardening, and verdict updates are also agent-run, not guaranteed on abnormal termination (`docs/feedback-loop.md`, cadence table and “Not shipped” list).

There is no recovery procedure for interrupted installs, corrupted wiki state, incomplete sessions, invalid telemetry records, or partial eval runs; no backup/restore test; and no replay/idempotency mechanism. The sidecar appends directly to JSONL (`scripts/sidecar.sh`), while the installer writes outputs in place (`scripts/adapters.py`). An audit trail is only useful if failures cannot silently leave the workspace inconsistent and if the team can restore it.

## 10. Medium — Onboarding and maintenance documentation is already drifting

Some of the project’s own layout instructions do not match the tree. `README.md` depicts `adapters/`, `canonical/plugins/`, `wiki/raw/`, and a Copilot `~/.copilot` output; the actual inventory instead has `scripts/adapters.py`, no `canonical/plugins/` or `wiki/raw/`, and no installer output to `~/.copilot`. The installer’s actual output paths are in `scripts/adapters.py`. More seriously for a new maintainer, `docs/toolchain.md` points to canonical files such as `canonical/skills/gitlab.md`, `canonical/mcp/coralogix.json`, and `canonical/mcp/atlassian.json` that are absent from the `canonical/` inventory. Those rows read as actionable setup guidance but cannot be followed as written.

The repository also gives one happy-path setup and troubleshooting table (`docs/setup.md`), but no maintainer guide for changing adapters, testing a new CLI release, rotating credentials, reviewing imported capability updates, cleaning generated output, or handing ownership to another person. `AGENTS.md` demands recurring wiki hardening, but no automation enforces it. The author can operate this research workspace; the docs do not yet let a new owner reliably operate and maintain it.

## Maturity: 3/10

**Demo/research-grade:** yes. The canonical-to-native adapter exists; important skill discovery and invocation paths have live evidence; the eval work distinguishes disk grading from model self-report; and the ledger records refutations and caveats rather than laundering them into successes. Those are real strengths and more than a slideware demo.

**Team-grade:** no. The project cannot currently promise reproducible dependencies, safe installation into pre-existing configs, rollback, privacy-safe telemetry, isolated eval execution, CI-enforced cross-tool compatibility, bounded spend, or conflict-safe shared operation. Several key lifecycle steps depend on agents remembering instructions; one target tool’s failure hook is known not to work; documentation references nonexistent capability files. A serious team could pilot this with an owner and strict local review, but should not adopt it as a trusted shared setup or standardize it across developers until the high-severity gaps have owners and enforceable controls.
