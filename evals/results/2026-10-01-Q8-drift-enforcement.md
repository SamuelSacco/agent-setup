# Q8 drift enforcement — results

Date: 2026-10-01 ET. Branch: `feat/drift-enforcement` from `origin/master` at 2abc02b. Prereg: `evals/results/2026-10-01-Q8-prereg.md`. Metered spend: $0 (no model eval sessions; code + local runs only).

## What was built

Enforcement tooling designed in `docs/install-scopes-2026-09-30.md` §3/§4, now working code:

- `scripts/drift_check.py` — stdlib-only Python, subcommands:
  - `collisions [--home DIR] [--project DIR]` — skill names (directories, or flat `<name>.md`) present at both global scope (`<home>/.agents/skills`, `<home>/.claude/skills`) and project scope (`<project>/.agents/skills`, `<project>/.claude/skills`). Exit 1 naming each collision with both locations; 0 when clean. Hazard is install-scopes §1a: Claude global-wins, Copilot project-wins.
  - `secrets [--root DIR]` — walks the tree (skips `.git`, binary files by NUL sniff, files > 1 MiB) for `sk-ant-...`, `ghp_`/`gho_`/`ghu_`/`ghs_`/`ghr_`/`github_pat_...`, `AKIA...`, `-----BEGIN ... PRIVATE KEY-----`, and high-entropy assignment lines. Assignments are restricted to SCREAMING_SNAKE / snake_case KEY/TOKEN/SECRET/PASSWORD/CREDENTIAL names with literal values (Shannon entropy ≥ 3.5, ≥ 2 character classes, placeholder markers excluded) — camelCase attributes, Python kwargs, and function-call values are code, not assignments; the first version flagged 11 such lines in this repo, the restriction brought the real-repo scan to 0 without an allowlist entry. Findings print `file:line` plus a 6-char prefix + `…[redacted]`; the full matched secret is never printed (asserted by the self-test). Allowlist: `.drift-allow` at the root, one path per line, `#` comments.
  - `pins [--root DIR]` — (a) re-hashes every entry in `canonical/skill-pins.json` (SHA-256), reusing `load_pins`/`sha256` from `scripts/import_skill.py` (X6); missing pins file = no pins recorded = pass, matching `import_skill.py verify` (master records no pins). (b) Every MCP package spec in `canonical/mcp/*.json` must carry an exact version pin (`\d+\.\d+\.\d+...`); `@latest`, ranges, and bare names are flagged and named. Package-shaped tokens in `scripts/adapters.py` are scanned the same way (currently none). All 5 canonical MCP specs pass (context7 4.1.1, filesystem 2026.8.31, github 2025.4.8, playwright-mcp 0.0.83, sequential-thinking 2026.8.31).
  - `all` — collisions + secrets + pins against the repo root with real HOME/project defaults; one-line summary per check; exit 1 if any check fails. Weekly verify entry point.
- `scripts/verify-weekly.sh` — bash wrapper, `exec`s `drift_check.py all` and propagates its exit code. Stable path for a weekly cron (no cron created by this item).
- `scripts/test_drift_check.py` — self-test, stdlib only. Fixtures in a temp dir under the workspace, removed on exit. Plants are assembled from string fragments so the test source itself contains no secret-shaped literal (the first version did, and the real-repo scan correctly flagged it).

Deliberately out of scope, unchanged: wiring into `scripts/install.sh`; canonical skill contents; creating `canonical/skill-pins.json`.

## Self-test output (verbatim)

```
PASS collisions: planted name at both scopes exits 1 and is named
PASS collisions: disjoint scopes exit 0
PASS secrets: planted fake secret exits 1 with file:line
PASS secrets: full secret never printed (redaction)
PASS secrets: allowlisted file exits 0
PASS secrets: clean fixture exits 0
PASS secrets: high-entropy KEY/TOKEN assignment exits 1 with file:line
PASS pins: correct pin + exact MCP pin exit 0
PASS pins: tampered pinned skill exits 1 and is named
PASS pins: @latest and bare unpinned MCP specs exit 1 and are named
PASS all: real repo tree exits 0

11/11 cases PASS
```
Exit code: 0.

## Real-repo run (verbatim, `./scripts/verify-weekly.sh`)

```
collisions: OK (0 collision(s), home=/home/hatch, project=/home/hatch/workspace/w5b-drift)
secrets: OK (0 finding(s), root=/home/hatch/workspace/w5b-drift)
pins: OK (0 skill pin(s), 0 finding(s), root=/home/hatch/workspace/w5b-drift)
all: OK — all checks clean
```
Exit code: 0. Note: HOME in this sandbox is the agent home (no global skills installed), so the collisions leg is vacuous here; the plant cases in the self-test are the collision proof.

## Known limits

- Secrets scan is pattern + entropy based: unquoted values containing `.`/`$`/`(`/`)` (expressions, env references) are not treated as literals, so a bare unquoted dotted token would be missed; quoted values and the named token shapes are covered. Passphrases with spaces are out of the assignment rule.
- Collisions covers `.agents/skills` + `.claude/skills` at both scopes per the brief; Copilot-only `.github/skills` / `~/.copilot/skills` are not scanned.
- Pins leg (a) is vacuous until a skill is imported with `import_skill.py` on a machine and the pins file committed.
- Plugin marketplace commit-SHA pinning (§3) has no canonical record on disk to verify against — not checked; MCP + skill pins only.
- Not wired into `install.sh` and no weekly cron created — both are follow-ups.
