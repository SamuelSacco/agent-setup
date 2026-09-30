# Cold-start usability critique

## Verdict

The repository's **skills** path is the strongest part of the shared-setup story, but “clone, install, both tools behave the same” is not a reliable cold-start promise. The README skips a clone command, the setup guide's “install” step only checks whether binaries exist, the installer can report success before either CLI can run, and several advertised capabilities are either manual or known not to work in Copilot. A competent engineer can get a basic prompt running, but not confidently get the documented, shared system working from these instructions alone.

## Findings (ordered by severity)

### High — The documented “from zero” path does not install the tools, and the README does not actually clone the repository

The README's step 1 says “Clone and enter the root” but runs only `cd agent-setup`; it never supplies a `git clone` command. The more complete `docs/setup.md` does have a clone command, but step 1, “Install the tools,” runs only `claude --version` and `copilot --version`. Those commands fail if the tools are absent; the Claude comment points to a homepage, and no Copilot installation instructions are given. The document therefore cannot take a stranger from zero to installed CLIs, despite explicitly claiming that scope. (`README.md:9-18`; `docs/setup.md:3-13,27-31`)

There is no supported OS or minimum-version matrix, and no upfront dependency check. `install.sh` requires Bash and `python3`; the generated MCP entries all run `npx`, which additionally requires Node/npm and network access when servers start. None is named in the quick start, and `claude --version` / `copilot --version` establish neither version compatibility nor MCP readiness. (`scripts/install.sh:1-6`; `canonical/mcp/*.json`; `docs/tips-copilot.md:37-47` records observations on Copilot v1.0.89, not a support floor.)

**Cold-start consequence:** if either CLI is missing, the reader is stranded at the first step. The claim of “~15 minutes” is credible only if both CLIs are already installed, the user already has service access, and the machine is otherwise prepared. (`docs/setup.md:3,5-13`)

### High — “Install complete” is not a working-install check; first-run prerequisites and credentials are deferred or undiscoverable

The installer just changes to the repository root, runs `python3 scripts/adapters.py`, and prints “Install complete.” It does not check that either agent CLI is installed or authenticated, that `npx` is available, that the project is trusted, or that any generated skill/agent/MCP server is discoverable. The adapter itself explicitly says discovery is unverified until an authenticated run. Thus a green completion message can mean only that files were written, while the first actual launch still fails or asks the user to solve new setup problems. (`scripts/install.sh:3-6`; `scripts/adapters.py:151-157`)

All five MCP definitions use `npx`, so the first MCP startup may need package downloads and network access; the docs do not warn that this happens after installation. More concretely, `canonical/mcp/github.json:8-10` configures `GITHUB_PERSONAL_ACCESS_TOKEN` as an empty string. `docs/toolchain.md` says secrets belong in a secure config or environment, but neither the quick start nor setup explains how to inject a token into this server without editing a generated file that the project says not to hand-edit. The user discovers the gap only when trying the GitHub MCP. (`README.md:11-24`; `docs/setup.md:34-41`; `docs/toolchain.md` “Auth rules”; `scripts/adapters.py:93-111`)

### High — The shared-agent adapter drops canonical constraints, and Copilot custom agents do not inherit the shared instructions

The canonical agent format includes fields such as `model_hint` and `tools_hint`; for example, `code-reviewer` sets a model hint and a limited tool list. Both adapter branches emit only `name` and `description`, silently dropping those fields. The two generated agents therefore do not retain all of the behavior/permission intent in the supposedly canonical definition. (`canonical/agents/code-reviewer.md:1-5`; `scripts/adapters.py:74-90`; the code-reviewer source itself notes that these fields are stripped.)

There is a second Copilot-specific hole: the generated `.agent.md` frontmatter does not opt into repository instructions, while `docs/phase2-packet-2026-09-30.md` says Copilot custom agents do not inherit repo instructions automatically and require `include-custom-instructions: true`. The adapter never emits it. Invoking a generated Copilot agent can therefore bypass the shared `AGENTS.md` workflow (wiki orientation, session lifecycle, and working agreements) that the setup tells users both tools share. The docs do not identify this exception or offer a workaround. (`scripts/adapters.py:83-90`; `docs/phase2-packet-2026-09-30.md`, “Setup state after Phase 2”)

### High — The “both tools” hook/telemetry promise is known to fail on Copilot, even though install emits a Copilot hook

The README presents hooks as shared telemetry infrastructure, and the adapter prints that each hook goes to “claude + copilot.” But the emitted Copilot hook is `postToolUseFailure`; the adapter's own comment says the tested Copilot CLI v1.0.89 has no loader for that event and no events fired. The tips document additionally says repo hooks require directory trust, and shell failures do not trigger this event even on a trusted directory. The feedback-loop guide confirms that Copilot failure capture is partial and that the needed payload-parsing adapter is “identified, not built.” Claude's hook is proven; Copilot's is not equivalent. (`README.md:3-5,64-66`; `scripts/adapters.py:114-145`; `docs/tips-copilot.md:49-58`; `docs/feedback-loop.md:13-20`; `docs/claims-ledger.md`, S4)

This is more than a caveat in a specialist feature: the normal setup never tells a Copilot user to trust the directory, while trust is a prerequisite for hooks. Even after trust, the current failure hook does not capture the advertised Copilot shell failures. A user following only the quick start will reasonably infer telemetry is active when it is not.

### High — Re-running install can silently replace existing configuration

`install_mcp()` writes new `.mcp.json` and `.github/mcp.json` files from scratch instead of merging existing server entries. `install_hooks()` preserves other top-level Claude settings but replaces the entire `hooks` object with the generated one. A user who adds a personal MCP server or existing Claude hook in those files loses it on every reinstall. The script has no backup, merge warning, or prompt; this is especially surprising because the documented workflow explicitly says to re-run it after editing canonical definitions. (`scripts/adapters.py:93-111,141-149`; `docs/setup.md:39-41`; `docs/feedback-loop.md:61-69`)

### Medium — The setup path omits trust and write-approval decisions that its expected result needs

After authenticating and installing, `docs/setup.md` asks the user to launch a tool and expects it to create a session file. That requires the agent to write to the repository, but the step does not say to approve the write or explain the permission model. The demo script acknowledges that Claude may ask for approval and says to allow it; this is a real manual intervention missing from the onboarding path. (`docs/setup.md:43-53`; `docs/demo-script.md:22-28`; `docs/tips-claude.md:67-70`)

Copilot's hook path has an additional trust gate, and headless runs do not necessarily ask about trust. The only instructions explaining this are buried in tool-specific tips, not surfaced at install or first launch. Nor does the setup explain which approvals to grant to MCP servers or what to do if a prompt is suppressed. (`docs/tips-copilot.md:49-53`)

### Medium — The wiki is instructed, not self-maintaining or cross-tool automatic

The README says both tools “write sessions” and “maintain the wiki,” while the setup's expected first run treats session creation as a result of simply asking the agent to orient. In reality, the start/end lifecycle is a set of instructions in `AGENTS.md`; session logs are agent-run, and `session-harden` must be invoked at close. The feedback-loop guide explicitly labels these steps agent-run, not automatic, and says Copilot session-end auto-invocation is unverified. There is no startup/session-end integration in the install path that enforces the lifecycle. A user who assumes ordinary sessions will be captured or hardened without explicitly asking is likely to find an empty or incomplete shared history. (`README.md:23-24,62-63`; `AGENTS.md:9-37`; `docs/setup.md:49-53`; `docs/feedback-loop.md:9-11,34-45,103-116`)

### Medium — The advertised canonical/plugin and adapter layout does not match what is shipped

The README documents `canonical/plugins/` and an `adapters/` tree of generated files, but the shipped canonical structure has no `plugins/` directory, and the adapter writes directly to `.claude/`, `.github/`, and root `.mcp.json`; it does not create an `adapters/` directory or install plugins. `AGENTS.md` also lists plugins as a supported capability type. This tells contributors there is a canonical extension surface that does not exist and misdirects them about where generated output lives. (`README.md:31-45`; `AGENTS.md:60-69`; `scripts/adapters.py:74-149`; actual `canonical/` contents)

### Medium — Setup completion criteria contradict the shipped evidence and make validation feel like required repair work

After a first prompt, setup says to run E1, E4, and E2, update the claims ledger, and considers setup “done” only when E1/E2 “flip to PROVEN.” But the same repository's ledger already marks the skill parity and cross-tool continuity claims PROVEN, while E4 is explicitly partial for Copilot. No command for running those E1/E2/E4 probes is given in `docs/setup.md`; the detailed demo script describes a live demonstration, not a newcomer validation procedure. This leaves a stranger unsure whether the install failed, whether they must reproduce project research, or what “done” means. (`docs/setup.md:55-59`; `docs/claims-ledger.md`, S1/S2/S4; `docs/demo-script.md:13-44`)

## Walk-through: what a cold user actually has to do

1. **Get the repo:** the README tells the reader to `cd` into a presumed checkout; only the longer setup guide provides a placeholder clone command. If the tools are not already installed, the next “install” step only runs version commands.
2. **Authenticate:** the setup guide provides `claude auth login` and `copilot login`, and correctly warns that `gh auth` alone is insufficient for Copilot. It does not state supported CLI versions or cover how to obtain/install the CLIs in the first place. (`docs/setup.md:15-24`)
3. **Run the installer:** this requires Bash and Python 3, but the actual MCP clients require `npx`/Node, network access, and—in the GitHub MCP case—a non-empty token. The installer verifies none of these and can still say “Install complete.” (`scripts/install.sh:1-6`; `canonical/mcp/*.json`)
4. **Launch and trust:** the setup expects a session file to appear but does not call out repository trust, file-write approvals, or manual session-hardening. Hooks are especially trust-sensitive in Copilot, and the emitted Copilot failure hook is known not to work. (`docs/setup.md:43-59`; `docs/tips-copilot.md:49-58`)
5. **Validate parity:** E1/E2 are already listed as proven; E4 cannot prove parity because Copilot failure capture is refuted/partial. The guide gives no simple, fresh-clone smoke test that separates a broken install from an unsupported feature.

## What a stranger cannot accomplish from these docs alone

- Install either CLI on a machine that does not already have it.
- Know the minimum supported Claude Code/Copilot versions or supported operating systems.
- Prepare the full runtime dependency set before invoking MCP (Bash, Python, Node/npm, network).
- Configure a usable GitHub MCP credential through a documented secret-safe route.
- Know how to approve/trust the repository and grant the file writes required for session logging.
- Obtain equivalent failure telemetry in both tools, or make generated Copilot custom agents inherit the shared workspace instructions.
- Safely preserve existing MCP servers and Claude hooks when rerunning the installer.
- Run the setup guide's stated E1/E2/E4 completion checks from documented commands.

## Realistic time to first success

For a user with repository access, both CLIs already installed, accounts ready, and a supported shell environment, budget roughly **20–30 minutes** to authenticate both tools, resolve first-run trust/permission prompts, install the generated files, and verify a useful capability. The guide's ~15-minute estimate is optimistic: the demo notes separately reserve 15 minutes for auth smoke-testing, and the MCP dependency/token issues remain after that. For a genuinely fresh machine, **30–60+ minutes** is a more realistic allowance, with high variance because the documentation does not provide CLI installation steps or a supported-platform path.

**Most likely kill step:** `docs/setup.md` §1. It is labeled “Install the tools” but only asks for `--version`; a stranger without preinstalled binaries cannot proceed. If they happen to have both CLIs, the next likely stall is first MCP startup: missing `npx`/network or the empty GitHub token, after an installer that has already declared success.
