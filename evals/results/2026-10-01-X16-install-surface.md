# X16 install-surface probes — results (2026-10-01, Wave 4-B)

Item: Q6 / X16. Prereg: `evals/results/2026-10-01-X16-install-surface-prereg.md`
(committed 5650e0e before any probe run). Cap $0.75; spend $0.00 (CLI/file
ops only, no model session in either probe). Versions: Claude Code
2.1.286, skills CLI 1.7.0, Node v24.20.0. Isolation: scratch HOME
`~/workspace/w4b-x16-scratch/home/` for every probe command; real
`~/.claude` verified untouched (no `claude-plugins-official` entry in
real settings after the run). Scratch tree deleted after evidence capture.

## Probe 1 — Claude remote (GitHub) marketplace: PROVEN

Commands as run (cheatsheet §5, unchanged; `HOME=<scratch>`):

```bash
claude plugin marketplace add anthropics/claude-plugins-official \
  --sparse .claude-plugin plugins/commit-commands
claude plugin install commit-commands@claude-plugins-official --scope user
claude plugin list --json
claude plugin details commit-commands@claude-plugins-official
```

- Add: exit 0. Output: "SSH not configured, cloning via HTTPS:
  https://github.com/anthropics/claude-plugins-official.git … ✔
  Successfully added marketplace: claude-plugins-official (declared in
  user settings)". `marketplace list` shows "Source: GitHub
  (anthropics/claude-plugins-official)" — remote source, not `directory`.
- Install: exit 0, scope user.
- Files landed (all under scratch HOME):
  - Payload: `.claude/plugins/cache/claude-plugins-official/commit-commands/ab024cdcfa7c/`
    (cache key = git SHA `ab024cdcfa7c`, matching `plugin list` version
    field) containing `.claude-plugin/plugin.json`, `LICENSE`,
    `README.md`, `commands/{clean_gone,commit,commit-push-pr}.md`.
  - `.claude/settings.json`: `extraKnownMarketplaces.claude-plugins-official.source
    = {source: "github", repo: "anthropics/claude-plugins-official",
    sparsePaths: [".claude-plugin", "plugins/commit-commands"]}` and
    `enabledPlugins: {"commit-commands@claude-plugins-official": true}`.
  - `.claude/plugins/known_marketplaces.json` records the same github
    source + `installLocation` under the scratch marketplace cache.
- Recognition: `plugin list --json` → one entry, `scope: user,
  enabled: true`, installPath = payload path above. `plugin details`
  returns the inventory: Skills (3) clean_gone, commit, commit-push-pr;
  always-on ~71 tok. All four prereg criteria met.

Mechanism note: no auth was demanded — the public repo cloned over
anonymous HTTPS after the CLI found no SSH config in the scratch HOME.

## Probe 2 — `npx skills --copy` mode: PROVEN

Commands as run (`HOME=<scratch>`):

```bash
npx -y skills add dbos-inc/agent-skills -g -y --copy \
  --agent claude-code github-copilot --skill dbos-python
npx -y skills list -g
```

- Add: exit 0 (the PROVEN symlink-mode run exited 2; copy mode does
  not). Installer summary, verbatim lines: "~/.agents/skills/dbos-python
  — copy → Claude Code, GitHub Copilot"; "✓ dbos-python (copied) →
  ~/.claude/skills/dbos-python, → ~/.agents/skills/dbos-python".
  GitHub clone phase took ~3.5 min wall (spinner); install itself
  completed normally.
- Copied, not linked: `find <scratch>/.agents/skills
  <scratch>/.claude/skills -type l` returns nothing. Both targets are
  real directories of regular files (41 files each).
- Targets:
  - Canonical: `<scratch>/.agents/skills/dbos-python/` — real files.
  - Claude: `<scratch>/.claude/skills/dbos-python/` — real files, an
    independent copy (not a link to canonical).
  - Copilot: no `<scratch>/.copilot/skills/` was created. The
    installer's "copy → … GitHub Copilot" resolves through the
    canonical store: Copilot reads `~/.agents/skills` directly (the
    PROVEN discovery path, install-scopes §1a), so the canonical copy
    is Copilot's usable dir. `skills list -g` shows dbos-python at
    `~/.agents/skills/dbos-python`, source `dbos-inc/agent-skills`.
- Byte-for-byte: source cloned fresh into the scratch tree
  (`git clone --depth 1 https://github.com/dbos-inc/agent-skills`,
  skill at `skills/dbos-python`). `diff -r` source↔canonical: empty.
  Source↔Claude target: empty. Canonical↔Claude target: empty.
  SKILL.md SHA-256 identical in all three:
  `1a61535c8c8fe418ad862f8584182563c0d68dd94b895074c4d6fbf68cd6ac47`.
  One nuance: the source's `CLAUDE.md` is a symlink → `AGENTS.md`;
  both installed copies dereference it to a regular file with identical
  content (3,026 B) — content byte-identical, link structure not
  preserved. That is why installed dirs count 41 regular files vs the
  source's 40 regular files + 1 symlink.
- Lock: `<scratch>/.agents/.skill-lock.json` written (version 3,
  `skillFolderHash 1a22aa347e884fb89d9ad49bec2ff4a281346bf0`), same
  hash-only form as symlink mode.

## Verdicts

| Probe | Before | Now |
|---|---|---|
| Claude remote (GitHub) marketplace add/install | UNVERIFIABLE | **PROVEN** |
| `npx skills --copy` | DOCS-ONLY / UNVERIFIABLE | **PROVEN** |

Docs updated in-branch: backlog X16 closed; claims ledger gains S27;
`docs/install-scopes-2026-09-30.md` §1a `--copy` annotation and §1b
remote-source note amended. Cheatsheet §5's remote commands are now
backed by a live run (they were written from the local probe + docs).
