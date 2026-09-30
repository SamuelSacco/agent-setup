# P2 — Skills ecosystem scan

Date: 2026-09-30. Scope: the `npx skills` CLI / skills.sh ecosystem, popular
community skills, supply-chain posture, adoption candidates for A/B evals.
Method: ran the CLI in sandboxed HOMEs (`HOME=/tmp/sk/home*`), inspected the
resulting filesystems, queried GitHub API for repo stats, read skills.sh.
API spend: $0.00 (no model calls; npm/GitHub/web only).

## 1. The `npx skills` CLI (skills.sh)

**What / who.** `skills` on npm, v1.7.0 (latest dist-tag, checked today).
Maintainers: rauchg, quuu. Source repo: `vercel-labs/skills` (32,818 stars,
pushed 2026-09-28). Homepage: skills.sh. It is Vercel Labs' installer +
directory for the open Agent Skills format (SKILL.md spec; Anthropic's spec
lives in `anthropics/skills/spec/agent-skills-spec.md`). **PROVEN** (npm
registry metadata + repo).

**Commands.** `add`, `use` (one-off prompt, no install), `list`, `find`,
`remove`, `update`, `init`, `experimental_install` (restore from lockfile),
`experimental_sync` (node_modules → agent dirs). Sources: GitHub shorthand /
URL, GitLab, any git URL, local path, Notion skill pages. **PROVEN**
(`skills --help`, local run).

**Install mechanics — file-system evidence (all PROVEN, sandboxed runs).**

- Canonical store is `.agents/skills/<name>/` — project scope in the project
  root, global scope at `~/.agents/skills/<name>/`. Real files live there
  (SKILL.md + any bundled scripts/references).
- "Universal" agents — GitHub Copilot is classified as one — read
  `.agents/skills` directly. No per-tool directory is created for them.
- Claude Code gets a symlink: `.claude/skills/<name>` →
  `../../.agents/skills/<name>` (same shape at global scope under `~`).
- Exception: project install targeting ONLY Claude Code used `mode: "copy"`
  straight into `.claude/skills/` with no canonical copy. With both agents
  targeted, mode was "symlink" via `.agents/skills`. So the answer to "does
  `npx skills add` add the skill to both configs" is: yes by default, but
  the mechanism differs per tool — shared canonical dir + symlink for
  Claude, native read for Copilot — and a single-agent install silently
  changes the layout to per-tool copies. Drift risk if a team mixes modes.
- Detection: with `-a claude-code -a github-copilot` both targets installed
  cleanly. With NO `-a` in a bare sandbox HOME (no pre-existing agent
  config), the CLI still installed for Claude Code + universal — detection
  is not gated on the tool being installed; default agent set applies.
- Lockfiles: project `skills-lock.json` (v1, per-skill SHA-256
  `computedHash`); global `~/.agents/.skill-lock.json` (v3, source URL,
  skillPath, `skillFolderHash`). `skills update` re-pulls from source;
  hashes are recorded but nothing in the observed flow verifies a pinned
  hash before update — lockfile is bookkeeping, not a pin. **PROVEN** for
  format; the no-verify-on-update reading is from the lockfile contents and
  help text, not a tamper test — **UNVERIFIABLE** as a security guarantee.
- Install records carry a `security` object (see §3).

**Registries / indexes.** skills.sh is the primary directory: per-repo and
per-skill pages with install counts and a leaderboard ("8W Activity",
"Installs"). Counts seen today: mattpocock/skills 4.3M total,
microsoft/azure-skills ~4.3–4.9M, vercel-react-best-practices 757.7K,
web-design-guidelines 683.3K. Secondary indexes exist (SkillsMP,
claudemarketplaces.com, mcpmarket) per third-party landscape notes —
**UNVERIFIABLE** from here; counts are skills.sh telemetry, self-reported
by the installer's own pipeline — treat as popularity signal, not audit.
Note: the vercel-labs repo page also lists junk entries (1-install
"canary" duplicates of real skill names) — namespace noise is visible
even on the flagship repo's page. **PROVEN** (page read).

## 2. What developers actually install

Repo stats via GitHub API, 2026-09-30 (**PROVEN** as API output):

| Repo | Stars | Contents (verified listing) |
|---|---|---|
| obra/superpowers | 293,248 | 14 workflow skills: brainstorming, writing-plans, test-driven-development, systematic-debugging, verification-before-completion, subagent-driven-development, using-git-worktrees, executing-plans, code-review pair, writing-skills |
| mattpocock/skills | 272,549 | Category packs (engineering/productivity/misc): tdd, diagnosing-bugs, code-review, implement-spec, to-tickets, triage, domain-modeling, grill-me, handoff, teach |
| anthropics/skills | 179,093 | Official: pdf/docx/xlsx/pptx, frontend-design, skill-creator, mcp-builder, webapp-testing, canvas-design, claude-api, doc-coauthoring |
| vercel-labs/agent-skills | 31,750 | 9 skills: React best-practices/composition/native, deploy-to-vercel, web-design-guidelines, writing-guidelines |
| expo/skills | 2,641 | Official Expo team skills; install via skills CLI or Claude plugin |
| microsoft/azure-skills | 1,514 | ~20 Azure ops skills: azure-diagnostics, azure-deploy, azure-kusto, azure-reliability, azure-compliance… |

Pattern: the installs concentrate in (a) vendor-official packs
(Anthropic, Vercel, Microsoft, Expo) and (b) two practitioner workflow
packs (superpowers, mattpocock). The long tail is single-purpose vendor
CLI wrappers. Workflow-discipline skills (TDD, debugging, verification)
are the recurring category across independent authors — that is the
category our canonical set already bets on (tdd-workflow,
verification-loop), which makes head-to-head A/B the obvious test.

## 3. Supply-chain posture

**Threat model.** A skill is instructions the agent treats as trusted,
plus optionally scripts the agent runs with the user's shell. Markdown
alone is a payload: prompt-injection in SKILL.md needs no executable.
Three observed escalations:

1. Bundled scripts are common in top packs — the `deploy-to-vercel` skill
   I installed ships `resources/deploy.sh` + `deploy-codex.sh`. **PROVEN**
   (filesystem).
2. Runtime fetch defeats static audit: `web-design-guidelines` (683K
   installs) instructs the agent to fetch its rule set from a
   raw.githubusercontent URL before every review. The bytes you vetted
   are not the bytes that run. **PROVEN** (SKILL.md read on skills.sh).
3. Install/update channel: `npx skills add owner/repo` clones HEAD of a
   git repo; `skills update` re-pulls. No signing observed anywhere in
   the flow. **PROVEN** (runs + lockfile inspection).

**What vetting exists.**

- skills.sh runs three audit feeds; verdicts ride along in the install
  JSON: `security: {gen: "safe", socket: "0 alerts", snyk: "medium"}`
  observed on a real install (writing-guidelines). `gen` = skills.sh's
  own analysis, `socket` = Socket supply-chain scan, `snyk` = Snyk.
  Coverage is not universal: two vercel-labs skills installed earlier in
  the same session returned `security: null`. **PROVEN** both ways.
- Snyk's "ToxicSkills" study (Feb 2026, as widely cited): 3,984 skills
  audited, 36.82% with ≥1 security flaw, 13.4% with a critical issue,
  76 confirmed malicious payloads; corroborated by an arXiv technical
  report (2605.28588) on the same sample. Numbers are the study's, read
  via secondary sources — **PROVEN** the study exists and reports these
  figures; not independently re-derived here.
- Third-party scanners exist (Clawdex by Koi Security; community
  "vet-skill" audit skills). No gate is on by default: the CLI installs
  first and reports verdicts alongside, it does not block on them in
  anything I ran. **PROVEN** for observed runs (a "medium" Snyk verdict
  installed without friction).

**Risk verdict for a developer dropping one in.** Equivalent to running
an unreviewed shell script plus handing a stranger a standing instruction
sheet for your agent. Minimum viable vetting, in order: official-vendor
or established-author source; read SKILL.md AND every bundled script;
reject runtime-fetch instruction sets or pin their source; check
`allowed-tools` scope; prefer `--copy` installs of a reviewed snapshot
over symlinked live repos + auto-update.

## 4. Candidates for A/B evals (candidates only — nothing ported)

| # | Skill | Source | Why test it |
|---|---|---|---|
| 1 | test-driven-development | obra/superpowers | Head-to-head vs our canonical tdd-workflow; most-starred workflow pack |
| 2 | systematic-debugging | obra/superpowers | Measurable on seeded-bug tasks; discipline claim is falsifiable |
| 3 | verification-before-completion | obra/superpowers | Anti-fabrication guard; directly relevant after our E6 fabricated-test finding |
| 4 | tdd | mattpocock/skills (engineering) | Second TDD implementation — three-way vs #1 and ours |
| 5 | diagnosing-bugs | mattpocock/skills (engineering) | Practitioner debugging rival to #2; pick a winner on data |
| 6 | code-review | mattpocock/skills (engineering) | Review quality on seeded-defect code is scorable |
| 7 | skill-creator | anthropics/skills | Meta-test: do machine-generated skills beat hand-written ones |
| 8 | frontend-design | anthropics/skills | Official design skill; pairs with the UI/UX agent question |
| 9 | mcp-builder | anthropics/skills | Our setup ships MCP adapters; test if it improves server output quality |
| 10 | vercel-react-best-practices | vercel-labs/agent-skills | Most-installed single skill found (757.7K); rules-dir structure worth benchmarking |
| 11 | web-design-guidelines | vercel-labs/agent-skills | 683K installs AND a runtime-fetch design — test value and flag the pattern |
| 12 | azure-diagnostics | microsoft/azure-skills | Vendor-official ops skill; tests the "vendor pack" hypothesis outside frontend work |

## Bottom line for the setup

The ecosystem converged on exactly our architecture — one canonical
skill dir, per-tool shims — and `npx skills` implements it with
`.agents/skills` where we hand-roll adapters. Difference worth noting:
their canonical dir is also Copilot's native dir, so for Copilot the
"adapter" is free; our install.sh should treat `.agents/skills` as a
target, not a competitor. The gap is vetting: hashes recorded, audits
displayed, nothing enforced. A canonical/ import path that snapshots,
hash-pins, and audit-checks third-party skills is the piece the
ecosystem is missing and this project could own.
