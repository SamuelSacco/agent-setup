# Merge readiness — phase-2 → master — 2026-09-30

Audit W4, branch `audit/merge-readiness` off phase-2 @ 3556e46.
Method: fresh clone, disk verification, live runs. Claims in docs were
treated as unproven until checked.

## Verdict

**1 BLOCKER. Do not merge until B1 is resolved.** Everything else is
nits; the trivial ones are already fixed on this branch (see Fixes).

## BLOCKERS

### B1 — Packet claims a shipped `quickstart.sh`; no such file exists in the repo

- `docs/phase2-packet-2026-09-30.md:83-85` describes a "quickstart.sh
  prototype: one command, 0 decisions," with fresh-sim timings
  (30 s warm; 1m58 s cold).
- `find` across the tree: no `quickstart*` anywhere. `git log --all --
  '*quickstart*'` is empty — never committed on any branch.
  `scripts/` contains only adapters.py, install.sh, run-eval.sh,
  run_eval.py, seed_wiki.py, sidecar.sh.
- The script exists only in worker scratch:
  `~/workspace/phase2/onboarding/scripts/quickstart.sh` (outside the
  repo). The timings may be real; the artifact is not in the merge.
- Resolution (Samuel's call): (a) land the script under `scripts/`
  after review, or (b) amend the packet bullet to state the prototype
  was scratch-only and is not shipped. Either closes B1.

## Fresh-consumer path (measured)

- Method: `git archive phase-2` → clean dir, fake HOME, run
  `./scripts/install.sh`.
- install.sh: exit 0, **0.09 s**, prints 8 skills / 12 agents /
  5 MCP / 1 hook (matches packet counts). Writes nothing to HOME.
- Tree delta after install: **zero files**. Regeneration is
  byte-identical to the committed `.claude/` + `.github/` outputs —
  install is idempotent on phase-2. (The packet's "install.sh dirties
  the tree (32 paths)" bullet is labeled V1 friction; it no longer
  holds — see N9.)
- Regen-from-scratch (`.claude/` + `.github/` deleted, re-run):
  exit 0, all outputs restored byte-identical except one file — N6.
- `scripts/quickstart.sh`: absent (B1). `scripts/run-eval.sh`:
  present, executable.
- `.github/mcp.json` uses `mcpServers`; root `.mcp.json` key is
  `mcpServers` — the Phase 2 adapter fix is in the generated output.

## Secrets scan

- Tree + full phase-2 history (29 commits, `git log -p` pattern
  scan): **no live API keys, tokens, passwords, or private keys.**
- Placeholders only: `sk-abc123` marked `// BAD` in a code-reviewer
  example (`.claude/agents/code-reviewer.md:260`,
  `.github/agents/code-reviewer.agent.md:260`,
  `canonical/agents/code-reviewer.md:262`);
  `COPILOT_PROVIDER_API_KEY=<redacted>` in
  `evals/fixtures/p2-port-verification/pv-copilot.sh:8`.
- One personal email: Samuel's own Gmail at
  `docs/morning-review-2026-09-30.md:25`. Same identity as the repo
  owner; repo is private. Info only.
- Absolute sandbox paths (`/home/hatch/...`) appear in eval fixtures
  and result transcripts (e.g. `evals/fixtures/p2-port-verification/
  pv-*.sh`, `docs/demo-backup/E6-pilot-copilot-fabrication.txt:67,75`)
  and in the proof-run block of `docs/feedback-loop.md:125,129`.
  They leak this sandbox's layout, not credentials. In transcripts
  they are recorded evidence; in feedback-loop.md they read as a
  runnable example a consumer cannot run. Post-merge cleanup
  candidate, not a gate item.

## Wiki / ledger hygiene

- Claims ledger: S1–S17 all present, sequential, **unique**
  (S6a/S6b are intentional sub-rows of S6). S16 = Copilot orientation
  UNVERIFIABLE, S17 = eval runner PROVEN. No duplicates after
  today's merges.
- `wiki/index.md`: every real `[[wikilink]]` resolves (notes live in
  `wiki/notes/`). The two `[[note-id]]` hits are inside HTML comments
  (index.md:13,38) — template examples, not links.
- `wiki/log.md`: every session file it references exists. Two
  session files on disk are not referenced in log.md:
  `wiki/sessions/2026-09-30-0124-claude-code-changelog-research.md`,
  `wiki/sessions/2026-09-30-0125-muse-copilot-cli-docs-research.md`
  (plus TEMPLATE.md, expected). N7.

## Git state

- Divergence: phase-2 = master + 29 commits, 0 behind. Diff:
  99 files, +11,786 / −3. Tree: 230 files, ~1.7 MB.
- No blob >5 MB in the tree or in any reachable history.
- No tracked build artifacts or caches (no `__pycache__`, `.pyc`,
  `node_modules`, `.venv`, `dist/`, `build/`).
- CLAUDE.md state at audit time: `@AGENTS.md` bridge present
  (Samuel's delete-vs-keep ruling still open; not an audit item).

## NITS

- **N1 (fix before presenting, not before merging)** — `docs/deck.html`
  ~line 206 states a session-end hook "invokes the cleanup skill
  automatically" as fact. Phase 2 verdict: automatic session-end
  triggering is NOT proven in either tool; the packet says "Do not
  upgrade this claim on stage." Deck otherwise tags its claims
  honestly (line 141 UNVERIFIABLE matches ledger S3; line 142 PARTIAL
  matches S5). Call: keep deck + script as dated V1 artifacts, marked
  superseded — done on this branch (HTML comment in deck.html,
  note in demo-script.md). Do not present from the deck until the
  line-206 claim is corrected or cut.
- **N2** — `README.md` layout listed `adapters/` and
  `canonical/plugins/`, neither of which exists. FIXED on this branch
  (layout now shows the real `.claude/` + `.github/` generated dirs).
- **N3** — `README.md` quickstart omitted the clone command (the
  packet itself records this as V1 friction). FIXED on this branch,
  using setup.md's `<this-repo>` placeholder convention.
- **N4** — `wiki/raw/` is referenced by AGENTS.md §3, README,
  `wiki/data-model.md`, and `wiki/index.md` but did not exist.
  FIXED: `wiki/raw/.gitkeep` added.
- **N5** — `docs/feedback-loop.md` carried the heading
  `### Proof run (this branch, 2026-09-30)` twice in a row. FIXED
  (one instance removed). Its `/home/hatch` proof block: left as-is
  (recorded run), see Secrets scan note.
- **N6** — `scripts/install.sh` (adapters.py) does not regenerate
  `.github/muse-instructions.md`; deleting it and re-running
  install restores everything else byte-identically but not that
  file. Fresh clones are unaffected (the file ships in the tree).
  Flagged; generator change is not a trivial fix.
- **N7** — Two session files unreferenced in `wiki/log.md` (see
  Wiki section). Flagged only; backfilling an append-only log is a
  judgment call.
- **N8** — `docs/toolchain.md:12-20` names nine canonical files
  that do not exist (skills: gitlab, db-shell, okteto, coderabbit;
  MCP: coralogix, mongodb, atlassian, chrome-devtools, figma).
  Mitigated by the file's own banner: entries describe the mechanism,
  live verification UNVERIFIABLE. Editorial call (mark rows as
  planned, or drop the paths) left to Samuel.
- **N9** — `docs/grill-prep.md:23,56` frames Copilot CLI precedence
  as a no-precedence combination. Phase 2 docs check superseded
  this: precedence is documented (first-loaded wins for agents and
  skills; last-loaded wins for MCP servers). Internal prep doc;
  update before reuse in Q&A prep.
- **N10** — Packet V1-friction bullets (install dirties tree, etc.)
  are labeled V1 history; the install one no longer holds on
  phase-2 (see Fresh-consumer). No edit — dated working document —
  but a merge reader should not quote them as current.

Checked and OK: `docs/demo-script.md` Act 3 hook line ("on the build
we tested it never fires. 0 of 5") is scoped to the tested build —
acceptable as written. `docs/setup.md` commands all exist
(`git clone`, `./scripts/install.sh`, `claude auth login`,
`copilot login`); its step order matches install.sh behavior.

## Fixes applied on this branch

README layout (N2), README clone line (N3), `wiki/raw/.gitkeep`
(N4), feedback-loop duplicate heading (N5), superseded markers on
deck.html + demo-script.md (N1). Plus this report and its session
record. No other files touched.

## Spend

$0 (no API-key eval runs; audit used local tools only).
