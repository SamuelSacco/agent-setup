# P2 Onboarding — "drop this in" adoption path

Date: 2026-09-30. Branch: `phase-2-onboarding`. Method: fresh-developer
simulation in scratch dirs (fresh `HOME`, tool-less `PATH`, local clone
standing in for the GitHub remote), then a prototype `scripts/quickstart.sh`
run end-to-end against a second fresh simulation. Tools: Claude Code
2.1.285, Copilot CLI 1.0.89.

Simulation boundaries (honesty): clone was local (0.4 s); a GitHub clone adds
network time. Sandbox network runs through an env-configured proxy —
stripping env (`env -i`) broke npm TLS (`ERR_SSL_WRONG_VERSION_NUMBER`);
that failure is a sandbox artifact, not a user-machine expectation. Auth
stood in via Claude `apiKeyHelper` and Copilot BYOK env; the browser OAuth
flows a stranger runs are the same gates, different mechanism — the gate
behavior is what was tested.

## 1. V1 walk, as a stranger (timed)

| Step | V1 instruction | Measured | Friction |
|---|---|---|---|
| Get the repo | README says `cd agent-setup` — the clone command is not in the Quick start; it lives in setup.md §3 with the URL as `<this-repo>` | 0.4 s local | F1: README Quick start assumes the clone already happened. F2: repo is **PRIVATE** — a developer without access cannot clone at all. Distribution is gated before step 1. |
| Install the CLIs | setup.md §1 shows `claude --version` / `copilot --version` and a URL comment — no install command for either tool | npm route measured: claude 19 s, copilot 41 s | F3: the two hardest installs are the ones the docs don't give. A stranger leaves the repo for two vendor doc sites. |
| Prerequisites | unstated | — | F4: `install.sh` needs python3; all 5 MCP servers are `npx -y` (node + network on first launch). Neither prerequisite is named anywhere in README/setup.md. |
| Authenticate | setup.md §2: `claude auth login`, `copilot login` | not timed (browser flow) | F5: two human browser flows, un-automatable, correctly flagged in the doc — but they sit *before* the clone in setup.md and *after* it in the README order. The two docs disagree on sequence. |
| Install capabilities | `./scripts/install.sh` | 0.1 s; materializes 8 skills, 12 agents, 5 MCP, 1 hook into both tools | F6: install **dirties the git tree — 32 modified/untracked paths**. Generated adapter outputs are half-committed, half-not; a fresh clone + install leaves a stranger staring at a filthy `git status` on minute one. Fix: gitignore generated outputs or commit them all. |
| First session | "launch from root, ask it to orient" | — | F7: nothing tells the stranger the setup is *project-scoped* — the "install" lives and dies with this repo root. Launch from any other directory and the system silently isn't there. |
| MCP first launch | implicit | not timed | F8: `canonical/mcp/github.json` ships `GITHUB_PERSONAL_ACCESS_TOKEN: ""` — the github server will fail until a human fills it in. Playwright MCP will try to launch Chrome. Neither is mentioned in setup.md. |
| Copilot first run | implicit | payload extraction 7.3 s on first invocation | F9: minor, one-time. |
| Prove it | setup.md §6: run evals E1 → E4 → E2 | evals take real runs + scoring | F10: "prove it" as designed is a research protocol, not a smoke test. A demo adopter will never do it. There is no cheap verification command in V1. |

Machine time in V1 is not the problem: ~1 min of commands total. The cost
is **decisions and absences**: 2 doc sites, 2 auth flows, 1 token to fill,
1 silent scoping rule, 0 verification commands. setup.md's "~15 minutes"
is really "15 minutes if you already know everything it omits."

## 2. Acquisition styles a 2026 developer expects

| Style | What each tool's native story assumes | Verdict |
|---|---|---|
| git clone + script (V1) | Developer trusts a repo, reads docs, runs a script. Both CLIs are external prerequisites the script doesn't manage. | PROVEN workable; friction table above. |
| npm / `npx`-style one-liner | The CLIs themselves are npm packages: `@anthropic-ai/claude-code` (19 s), `@github/copilot` (41 s) — both installed into a scratch prefix and ran at the expected versions. An `npx agent-setup` one-liner for *this setup* does not exist: no published package, and the repo is private. | CLIs via npm: PROVEN. `npx` for this setup: REFUTED as an existing option. |
| In-tool plugin install | Claude Code plugins are a marketplace flow driven inside the interactive UI; Copilot CLI exposes `plugin` / `skill` / `mcp` / `instruction` subcommand families (repo research, `docs/tips-copilot.md`). Both are per-tool: neither installs into the *other* tool, so the native stories cannot produce the dual-tool setup by themselves. Not driven headlessly here. | UNVERIFIABLE headlessly; structurally insufficient for dual-tool parity either way. |
| Standalone script (curl-style) | quickstart.sh copied outside any clone, run with `--repo`/`--dir`: clones, materializes, verifies. This is how runs 2–3 below executed. | PROVEN (below). |

Conclusion: the canonical clone stays the distribution unit (private repo,
org-internal), but the script must absorb everything around it — CLI
install, preflight, verification — because the native per-tool stories
structurally cannot.

## 3. Minimal path design

One command after clone (or one standalone script before it):

```
git clone <repo> agent-setup && cd agent-setup && ./scripts/quickstart.sh
```

Phases: preflight (git/python3 hard gates; node/npx warnings; missing CLIs
npm-installed into `~/.local`, no sudo) → workspace (in-clone detection or
clone) → `install.sh` → **structural verify** (materialized counts vs
canonical for both tools, both MCP configs parse — free, deterministic) →
**auth gate** (unauthenticated → print the exact login command, exit 2,
re-run resumes; nothing half-configures) → **live verify** (one headless
probe per tool; see §4).

Counts, cold machine, honest: **1 command line, 0 decisions, 2 unavoidable
human actions** (the two vendor auth flows), **1 advisory action** (add
`~/.local/bin` to shell PATH if the CLIs were npm-installed). Warm re-run:
~30 s. Cold run measured: 1 m 58 s including both npm installs, stopping
correctly at the auth gate.

## 4. The verification probe

A verify command is only worth anything if it can fail. Design rule:
**probe for skill-body facts, never skill names** — names appear in the
loaded skill *listing* (description line), so a name-level probe passes
even when the body never loaded. Probe v1 asked session-harden's "first
action"; Claude answered from the description text ("distill the current
session log into maintained wiki notes") — a false-positive PASS.
**Probe v1: REFUTED as a verification instrument.**

Probe v2 asks for two facts that exist only in the skill body (step 5 +
Rules): the never-edit directory (`wiki/raw/`) and the three final session
status values (`complete` / `partial` / `abandoned`). Results:
Claude PASS ($0.0124, 1 turn) and Copilot PASS under BYOK (16.8k input
tokens, 34 s) in simulation 1; PASS again inside quickstart runs 2c/3
($0.0035 / $0.0038, warm caches). **Probe v2: PROVEN** as a dual-tool
smoke check at ~$0.004–0.012 per tool per run.

## 5. quickstart.sh test log (simulation 2, fresh HOME + tool-less PATH)

| Run | State | Result |
|---|---|---|
| 1 | no CLIs, no auth | CLIs npm-installed, structural PASS, auth gate exit 2 with remedy. 1 m 58 s. PROVEN path. Two breaks found (below). |
| 2 | claude authed, copilot not | Claude probe FAILED — checker bug, not a setup failure. |
| 2b | same, warm | Same FAIL — reproducible, isolated. Root-caused to the checker. |
| 2c | same, checker fixed | Claude probe PASS ($0.0035); copilot classified unauthenticated → exit 2 with remedy. As designed. |
| 3 | both authed (copilot via BYOK) | Full PASS, exit 0, 30 s warm. `QUICKSTART COMPLETE`. |

Breaks found and fixed in the prototype:

1. **Swallowed installer errors.** First version discarded npm output; a
   failed install reported a bare FAIL with no cause. Fixed: npm log tail
   printed on failure. (The failure that exposed this was the sandbox
   proxy artifact, §0.)
2. **Stdin-starving checker.** `check_answer` ran four sequential `grep`s
   on one pipe; the first grep consumed the stream, later greps saw EOF —
   every live probe failed regardless of the answer. Isolated replication
   with a single grep passed, which is why it survived two runs. Fixed:
   read stdin once into a variable, grep the variable. A verification
   script that cries wolf is worse than none — this is the run that
   proves the failure classification (auth vs probe vs setup) matters.
3. **Bootstrap detection caveat (not fixed — documented).** Run from any
   existing clone, quickstart adopts that clone — including, in run 1, my
   own dev clone instead of the simulation target. Correct behavior for a
   stranger; surprising in a test harness. The standalone-copy shape
   (runs 2–3) is the distribution form that avoids it.

Auth-gate classification: Claude via `claude auth status` (deterministic,
pre-probe). Copilot has no equivalent status command in this flow — its
probe output is classified (`No authentication` → remedy + exit 2).
**Copilot auth pre-detection: UNVERIFIABLE** as a cheap deterministic
check on 1.0.89; probe-classification is the working substitute.

## 6. API spend (cap $2)

Claude-metered probes: $0.0153 + $0.0124 (sim 1) + $0.0035 (manual sim-2
debug) + $0.0035 (run 2c) + $0.0038 (run 3) = **$0.0386 recorded**, plus
one replication probe whose cost field was not captured (≈$0.004 by
sibling runs). Copilot BYOK probes are token-metered, not dollar-metered
(2 successful probes, ~17k input tokens each ≈ $0.02 each at Haiku
rates). **Total ≈ $0.08 of $2.** All runs Haiku
(`claude-haiku-4-5-20251001`), 1 turn each.

## 7. Recommendations (not implemented here)

1. Ship `scripts/quickstart.sh` as the README's step 1; demote setup.md
   to reference. Rewrite the README Quick start to include the clone.
2. Fix the dirty-tree problem: gitignore generated adapter outputs
   (`.claude/skills|agents`, `.github/skills|agents|hooks`, both MCP
   JSONs) or commit them fully. Half-committed is the worst state.
3. Either fill the github MCP token during quickstart (prompt once,
   write to a gitignored local override) or drop `github` and
   `playwright` from the default canonical set — a default that fails on
   first launch teaches adopters to ignore failures.
4. State the prerequisites and the project-scope rule in the first
   screen of the README: python3, node/npx, launch-from-root.
5. `docs/setup.md` §6's eval ladder stays as the *maintainer* protocol;
   adopters get probe v2. Don't make demo audiences run E1–E6 to trust
   the setup.
6. Distribution decision for Samuel: PRIVATE repo = invited humans only.
   For org-wide "drop this in," the repo needs internal visibility or a
   release artifact; no script fixes a 404.
