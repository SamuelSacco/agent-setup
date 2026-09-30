# W5 — CLAUDE.md-drop experiment — 2026-09-30

Question: can this repo drop `CLAUDE.md` (line 1 `@AGENTS.md` + "Claude Code only" annex) now that Claude Code ≥2.1.277 reads `AGENTS.md` natively?

Method: canary probes, headless. CLI `claude` 2.1.285, model `claude-haiku-4-5-20251001`, `--output-format json`, per-arm fresh `HOME`, project `.claude/settings.json` = `{"apiKeyHelper": "/home/hatch/workspace/skills/anthropic/bin/claude_api_key_helper.py"}`. Probe prompt (all arms, verbatim): quote verbatim every canary rule given in project instructions at session start, give the full token, name the source file; no tools.

Canaries per arm `<X>`: shared rule in `AGENTS.md` = token `W5-CANARY-<X>`, word `ZEPHYR-<X>`. Annex rule in `CLAUDE.md` = token `W5-ANNEX-<X>`, word `ANNEXWORD-<X>`.

Scratch location deviation, with reason: briefed location `~/workspace/p2/w5/scratch/` is inside this repo, whose own `CLAUDE.md` is an ancestor of every scratch project. Two runs there were contaminated and discarded (see Contamination). Clean runs: `/tmp/w5scratch/<arm>/run<N>/{project,home}`, no `CLAUDE.md`/`AGENTS.md` in any ancestor (`/tmp`, `/` checked).

## Results

| Arm | Setup | Run 1 | Run 2 |
|---|---|---|---|
| A (control) | `CLAUDE.md` = `@AGENTS.md` + annex (repo form) | shared ✓, annex ✓ | shared ✓, annex ✓ |
| B (drop) | no `CLAUDE.md` | shared ✓, annex absent (by construction) | shared ✓, annex absent |
| C (trap) | `CLAUDE.md` annex-only, no `@AGENTS.md` import | annex ✓, **shared ✗** | annex ✓, **shared ✗** |
| D (setting) | C's files + both-files setting in user settings (below) | shared ✓, annex ✓ | shared ✓, annex ✓ |

Model attributions were correct in every run (shared → `AGENTS.md`, annex → `CLAUDE.md`).

## Load evidence (beyond model self-report)

- B, both runs, `--debug-file` log: `[cc-plugin-agents-md] $.ui.log: no CLAUDE.md found; AGENTS.md loaded: /tmp/w5scratch/B/run<N>/project/AGENTS.md`.
- C run 1 transcript (`home/.claude/projects/-tmp-w5scratch-C-run1-project/*.jsonl`): 0 occurrences of `W5-CANARY-C` anywhere in the session file — the shared file never entered context. B run 1 transcript: 2 occurrences.
- A/B/C debug logs all carry: `plugin cc-plugin-agents-md: no pluginConfigs["agents-md@builtin" or "cc-plugin-agents-md@builtin"].options in user, --settings or managed settings (project settings are not read); every option is its default`. D logs omit this line and instead show `$.fs.ancestors (cc-plugin-agents-md): AGENTS.md, .claude/AGENTS.md found 1 of 5 directories`.

## Arm D setting — exact mechanism (headless-settable, PROVEN)

In user settings (`$HOME/.claude/settings.json`), not project/local settings (ignored there, per debug line above):

```json
{"pluginConfigs": {"cc-plugin-agents-md@builtin": {"options": {"instructionFiles": "claude-md-and-agents-md"}}}}
```

Effect in D: annex-only `CLAUDE.md` + native `AGENTS.md` both loaded, 2/2 runs. So the `/config` "Project instructions" mode is settable headlessly; it is per-user state, not shippable in the repo.

## Contamination finding (discarded runs, still evidence)

First A and B runs executed under `~/workspace/p2/w5/scratch/`:

- A run quoted both canaries but attributed the annex to two files: the scratch `CLAUDE.md` and the repo's own `/home/hatch/workspace/p2/w5/CLAUDE.md` (ancestor load).
- B run in that location: shared canary **not loaded**. Model reported only the ancestor repo `CLAUDE.md`. A nested `git init` in the scratch project did not stop the ancestor walk.

Consequence: the suppression check is "any `CLAUDE.md`/`CLAUDE.local.md` in cwd or any ancestor", and it applies to any working directory inside a tree that has one — including subdirectories of this repo if the root file were dropped but one existed higher up, and any parent project a user checks this repo into.

## Verdict

**PARTIAL.** "CLAUDE.md can be dropped" is:

- PROVEN for the shared instruction text, on this surface: Claude Code 2.1.285, direct Anthropic API, no `CLAUDE.md` in cwd or ancestors → `AGENTS.md` loads natively, complete, correctly attributed (arm B, 2/2, plus loader debug line).
- REFUTED as an unconditional drop: arm C proves any surviving `CLAUDE.md` without the import silently suppresses the native read (shared canary absent 2/2, 0 transcript hits). The drop is all-or-nothing per directory tree, not per file.
- Conditional on version/surface floor from research (`hidden_files/research/instructions-files.md` §2, not re-tested here): native read requires v2.1.277+, built-in `agents-md` plugin enabled; at introduction not on Bedrock/Vertex/Foundry; pre-2.1.281 some sessions (Bedrock, telemetry disabled) read CLAUDE.md only. The `@AGENTS.md` bridge has none of these gates.

## What breaks if dropped (exact list)

1. The annex content itself. Current `CLAUDE.md` annex, verbatim substance: (a) verify loading with `/context` (file appears under Memory files); (b) pointer that tool-native niceties (`/advisor`, output styles, `.claude/rules/`) are covered in `docs/tips-claude.md`. If the file is deleted without relocating these two items, both are gone. Note (a) also changes meaning: under native read the file to check in `/context` is `AGENTS.md`.
2. `InstructionsLoaded` hook firing. Per research §2 (documented, not re-tested in this run): hooks fire for `CLAUDE.md` and for an `AGENTS.md` imported by a `CLAUDE.md`; they do **not** fire for a natively read `AGENTS.md`. This repo's telemetry design (`AGENTS.md` §6) consumes hook events; dropping the bridge removes that event for the main instruction file.
3. Ancestor fragility (observed, above): after a drop, any stray `CLAUDE.md`/`CLAUDE.local.md` introduced in the repo root or a parent directory silently reverts that subtree to CLAUDE-only loading. Failure mode is silent — arm C's model reported the annex normally and never mentioned a missing file.
4. `--add-dir` case (research §2): with `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD` set, additional directories' `CLAUDE.md` loads; their `AGENTS.md` does not.
5. External-import approval semantics differ (research §2): `@path` imports from a natively read `AGENTS.md` load only if external imports were already approved for the project, with no prompt; from `CLAUDE.md` Claude asks first. Current repo `AGENTS.md` has no external imports; breaks only if added later.
6. Nothing else observed: load completeness of the shared file in B matched A (full rule quoted verbatim both runs); no partial load, no ordering artifact visible at this file size.

## V2 recommendation

Keep the bridge. `CLAUDE.md` = `@AGENTS.md` + annex costs one import line, never double-loads, fires `InstructionsLoaded`, and works on every version and surface including the ones native read excludes. The drop saves one 10-line file and buys a version floor, a silent-suppression failure mode, and a hook loss.

If the drop is wanted anyway, the minimum safe form is: delete `CLAUDE.md` and `CLAUDE.local.md` everywhere in the tree, move the annex into `.claude/rules/` (unscoped rules load at launch with `CLAUDE.md` priority and stay Claude-only), accept the `InstructionsLoaded` loss in the telemetry design, and pin Claude Code ≥2.1.277 (≥2.1.281 off the direct API) in the setup docs. Do not rely on arm D's setting for the repo: it lives in each user's `~/.claude/settings.json` and cannot be shipped.

## Cost log

Per-run `total_cost_usd` from `--output-format json`:

| Run | Cost |
|---|---|
| A1 | 0.01260115 |
| A2 | 0.01206615 |
| B1 | 0.01134865 |
| B2 | 0.01127365 |
| C1 | 0.01121365 |
| C2 | 0.01102865 |
| D1 | 0.01201865 |
| D2 | 0.01174865 |
| Clean subtotal (8 runs) | **0.09329920** |
| Discarded contaminated A (in-repo scratch) | 0.01379115 |
| Discarded contaminated B (in-repo scratch) | 0.01330865 |
| **Total spent** | **0.12039900** |

Cap $1.00; spent $0.1204.

Raw evidence (ephemeral, `/tmp`): `/tmp/w5scratch/<arm>/run<N>/out.json` (full JSON incl. result text), `debug.log`, `home/.claude/projects/*/*.jsonl` (transcripts), project files as constructed above.
