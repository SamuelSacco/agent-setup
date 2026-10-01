# X16 install-surface probes — preregistration (2026-10-01, Wave 4-B)

Item: Q6 / X16. Backlog: X16. Feeds: `docs/install-scopes-2026-09-30.md`
§1a/§1b, `evals/results/2026-09-30-P2-install-matrix.md` (the two
UNVERIFIABLE cells). Hard metered cap: $0.75 total. CLI probes; expected
model spend $0 (no model session is part of either pass criterion —
recognition is checked via `plugin list`/`details` and `skills list`,
not by invoking a model).

Base: `origin/master` 048e5ff at branch creation. Branch
`lab/x16-install-surface`. Versions on this machine at prereg time:
Claude Code 2.1.286, skills CLI 1.7.0, Node v24.20.0.

## Isolation (both probes)

- Scratch HOME: `~/workspace/w4b-x16-scratch/home/` (under `~/workspace`,
  never `/tmp`). All probe commands run with `HOME=<scratch>`,
  `PATH` unchanged. Claude config therefore lands in
  `<scratch>/.claude/`; skills canonical store in `<scratch>/.agents/`.
- Real `~/.claude`, `~/.copilot`, `~/.agents` are never written: probe
  commands carry the scratch `HOME` explicitly; pre/post check records
  that no probe path resolves outside the scratch tree.
- No credentials: if any step demands auth/a token, that probe stops
  and is recorded UNVERIFIABLE (blocked on credential). No stored
  credential is used.
- Scratch tree is deleted after evidence (paths + listings) is recorded
  in the results file; it is not committed.

## Probe 1 — Claude remote (GitHub) marketplace add + install

Prior state: local-directory marketplace add/install PROVEN (P2 matrix);
remote source UNVERIFIABLE (not tested). Cheatsheet §5 names the exact
commands; used unchanged.

Exact commands (cwd: scratch project dir, `HOME=<scratch>`):

```bash
claude plugin marketplace add anthropics/claude-plugins-official \
  --sparse .claude-plugin plugins/commit-commands
claude plugin marketplace list
claude plugin install commit-commands@claude-plugins-official --scope user
claude plugin list --json
claude plugin details commit-commands@claude-plugins-official
```

Pass (PROVEN) requires ALL of:
1. `marketplace add` exits 0 and reports the marketplace added; source
   recorded as a GitHub/remote source (not `directory`).
2. `plugin install` exits 0, scope `user`.
3. Payload on disk under
   `<scratch>/.claude/plugins/cache/claude-plugins-official/commit-commands/<version-or-sha>/`
   with the plugin tree present; `<scratch>/.claude/settings.json`
   carries `extraKnownMarketplaces` + `enabledPlugins` entries.
4. Recognition: `claude plugin list --json` shows the plugin with
   `scope: user, enabled: true`; `plugin details` returns a component
   inventory (not "not found").

Fail (REFUTED): add or install exits non-zero with a mechanism that is
not an auth/credential demand, or files/recognition contradict the
documented remote path. Auth demand → UNVERIFIABLE (blocked on
credential), per task rules.

## Probe 2 — `npx skills --copy` mode

Prior state: `--copy` DOCS-ONLY ("copies instead of symlinks");
default symlink fan-out PROVEN (install-scopes §1a). Same source repo
and skill as the PROVEN symlink runs, one variable changed (`--copy`).

Exact commands (cwd: scratch project dir, `HOME=<scratch>`):

```bash
npx -y skills add dbos-inc/agent-skills -g -y --copy \
  --agent claude-code github-copilot --skill dbos-python
npx -y skills list -g
```

Then file inspection (no model): `find` + `ls -la` + `file`/link checks
on `<scratch>/.agents/skills/dbos-python/` (canonical),
`<scratch>/.claude/skills/dbos-python` (Claude target),
`<scratch>/.copilot/skills/` if created (Copilot target), and a
byte-for-byte comparison: clone the source repo into the scratch tree
(`git clone --depth 1 https://github.com/dbos-inc/agent-skills`) and
`diff -r` the canonical skill dir and each target dir against the
source skill dir (excluding any CLI-written metadata files, named if
present).

Pass (PROVEN) requires ALL of:
1. Add exits 0 (note: the PROVEN symlink run exited 2 despite success —
   if exit is non-zero, the file checks below decide, and the exit code
   is recorded).
2. Claude target is a real directory of regular files, NOT a symlink
   (`test -L` false, `find -type l` empty inside it).
3. Canonical store holds real files; Copilot receives a usable skill
   dir — either it reads the canonical store directly (the PROVEN
   symlink-mode behavior; then canonical = Copilot's dir) or a real
   copied dir exists under a Copilot location. Which mechanism occurred
   is recorded either way.
4. Content matches source byte-for-byte: `diff -r` empty for canonical
   and for the Claude target (modulo named CLI metadata).

Fail (REFUTED): targets are symlinks despite `--copy`, a target tool
gets no usable dir, or content differs from source. Network/auth block
→ UNVERIFIABLE with the reason.

## Reporting

Results: `evals/results/2026-10-01-X16-install-surface.md` — per-probe
verdict (PROVEN / REFUTED / UNVERIFIABLE + mechanism), commands as run,
landing paths + listing evidence. Backlog X16 and any claims-ledger row
the matrix feeds updated in-branch. No merge; push branch only.
