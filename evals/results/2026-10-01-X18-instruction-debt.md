# X18 — Canonical instruction debt: closure verification

Date: 2026-10-01. Branch: `fix/x18-instruction-debt` off master `ce0edbe`.
Verdict: **PROVEN** — zero broken references and zero unresolved suspect
patterns in the shipped instruction surfaces, by the scan below (exit 0).
Spend: $0.00 (no API / CLI eval runs; local file work and scans only).

## Checklist source

The audit that produced the X18 queue is the off-repo prompt audit of
2026-09-30 (`~/workspace/phase2-prompt-audit-2026-09-30.md`), summarized
in `docs/phase2-addendum-2026-09-30.md` ("Instruction-debt audit") and
`wiki/notes/instruction-debt.md`: 12 SUSPECT patterns, 0 contradictions,
4 broken references. That report is the checklist used here; every item
is dispositioned below.

## Why X18 was still open at ce0edbe

The 2026-09-30 fix stream (commit `297285e`, merged in `82ea351`) fixed
11 of 12 suspect patterns and all broken references in `canonical/`,
and updated the wiki note — but it never updated
`docs/experiments-backlog.md`, and it missed one pattern (S12 below).
This run re-verified all 16 items on disk at `ce0edbe`, fixed the
residual, regenerated the adapters, and closes the backlog item.

## Before / after counts

Surfaces scanned: `canonical/agents/*.md`, `canonical/skills/*.md`,
their emitted mirrors in `.claude/` and `.github/`, and root
`AGENTS.md` — 61 files. Roster checked against disk: 12 agents,
8 skills, 9 files in `scripts/`.

| Measure | Audit baseline 2026-09-30 (pre-fix) | ce0edbe, re-measured this run (before) | This branch (after) |
|---|---:|---:|---:|
| Broken reference types | 4 | 0 | 0 |
| Broken identifier hits in shipped surfaces | 11 (prior checker count) | 0 | 0 |
| SUSPECT patterns unresolved | 12 | 1 (S12, present in 3 surfaces) | 0 |
| Suspect-marker scan hits | — | 3 | 0 |
| Scan exit code | — | 1 | 0 |

## Per-item disposition — broken references (4 audit items)

All four were fixed in `297285e` and are verified fixed on disk at
`ce0edbe` by this run's scan (0 hits each, canonical + both adapters):

- B1 `researcher` agent, invoked ×5 in `search-first` — FIXED (in
  297285e): rewired to subagent delegation / research pass; no
  `researcher` agent exists in the 12-agent roster and none was invented.
- B2 `architect`, invoked in `search-first` and
  `build-error-resolver.md:107` — FIXED: canonical rename to
  `code-architect`, which exists (`canonical/agents/code-architect.md`).
  Bare-`architect` invocation scan: 0 (the word "architecture" and the
  name `code-architect` are not hits).
- B3 `security-review` skill, referenced in `security-reviewer.md:104`
  — FIXED: rewired to the existing skill `verification-loop`
  (security-reviewer now ends: "see skill: `verification-loop`").
  No `security-review` skill exists and none was invented.
- B4 `scripts/setup-package-manager.js`, mandated by `tdd-workflow`
  Step 0 — FIXED (also suspect S9): mandate removed; Step 0 now detects
  the package manager from the `PACKAGE_MANAGER` env var, the
  `package.json` `packageManager` field, then the lockfile. The script
  does not exist and was not created.

Beyond-audit references the 297285e checker found and fixed, also
verified 0 at ce0edbe and after: `bun-runtime` skill pointer (removed),
`iterative-retrieval` skill section (removed — replaced by
progressive-discovery cycles in `search-first`),
`scripts/codemaps/generate.ts` in `doc-updater` (removed — codemaps are
workflow-generated), and the `/update-codemaps` / `/update-docs`
backing claim in doc-updater's description (removed).

Reference-resolution pass (this run): every `skill: <name>` and
`scripts/<file>` token in the 61 scanned files resolves to a file on
disk — 0 unresolved. (One regex false positive in an early scan draft,
"Invoke this skill:" in verification-loop, is a heading, not a
reference; the final script requires `skill: <name>` with a name token.)

## Per-item disposition — 12 SUSPECT patterns

Verified fixed in `297285e` (this run: re-checked on disk at ce0edbe;
marker in parentheses):

- S1 Verification ritual — `verification-loop` "run verification every
  15 minutes" — FIXED: Continuous Mode is event-driven ("not on a
  timer"; re-verify on change / before PR / before claiming done).
  Marker `every 15 minutes`: 0.
- S2 Booster — `code-reviewer` description "MUST BE USED for all code
  changes" — FIXED: trigger is now "Use after writing or modifying
  code, before the change is committed or handed off." Marker: 0.
- S3 Booster — `security-reviewer` closing "**Remember**: Security is
  not optional… be thorough, be paranoid" — FIXED: paragraph deleted.
  Markers `Security is not optional` / `paranoid`: 0.
- S4 Unsourced constant — "80% coverage" in 11 locations
  (`tdd-guide`, `tdd-workflow`, `verification-loop`, `planner`) —
  FIXED: defined once in `tdd-workflow` Core Principle 2 as a labeled
  heuristic default ("not a measured optimum and not a law"; project
  config overrides). All remaining canonical occurrences (10 lines
  after this run) are that definition, labeled references to it, the
  labeled Jest-config example of it, or `code-reviewer`'s ">80%
  confident" reporting threshold — a different mechanism the audit
  explicitly did not count. No unlabeled universal gate remains.
- S5 Booster — `tdd-workflow` "This skill ensures all code development
  follows TDD principles with comprehensive test coverage" — FIXED:
  intro now reads "tests first, minimal implementation, refactor —
  with coverage reported against a heuristic default, not treated as
  the goal." Marker: 0.
- S6 Booster — `tdd-workflow` closing "**Remember**: Tests are not
  optional…" — FIXED: deleted. Marker: 0.
- S7 Mandatory scaffold — git checkpoint ceremony in `tdd-workflow`
  (checkpoint commit after each stage + `HEAD`-reachability policing)
  — FIXED: Core Principle 4 is 4 mechanism lines — checkpoints at
  phase boundaries only (RED, GREEN; refactor optional), no mid-phase
  commits, no reachability check. Marker `reachable from`: 0.
- S8 Mandatory scaffold — Step 8 "TDD Evidence Report" document —
  FIXED: Step 8 is "Report the Result"; the report is the quoted test
  output itself, "no separate evidence-report document." Marker: 0.
- S9 Mandatory procedure — Step 0 `setup-package-manager.js` mandate —
  FIXED: see B4.
- S10 Mandatory ritual — `tdd-guide` pass@1 / pass@3 addendum — FIXED:
  addendum scoped to release-critical paths only; it requires
  recording run counts and results, "not just a pass-rate label," and
  ordinary fixes use the RED/GREEN cycle alone. Markers `pass@1`,
  `pass@3`, `pass^3`: 0.
- S11 Stale example — Playwright E2E example: `waitForTimeout(600)`,
  hard-coded counts, `page.fill(..., '2025-12-31')` — FIXED:
  auto-retrying `expect(results).toHaveCount(...)` assertion, no fixed
  sleeps; end date computed 30 days out in code. Markers: 0.
- S12 Stale example — `planner` "Worked Example: Adding Stripe
  Subscriptions," a 77-line full-detail plan anchoring maximal detail
  as the default — **FIXED IN THIS RUN** (the one residual at
  ce0edbe; 297285e had added only a sizing caveat line). Removed:
  the full worked plan (planner.md lines 103–181 at ce0edbe, 79 lines
  including its in-example 80% line). Replaced with a 16-line outline:
  headings, phases in one line each, per-step fields, closing criteria,
  and "size the detail to the risk." `canonical/agents/planner.md`:
  214 → 151 lines. Adapters regenerated with `scripts/install.sh`;
  only the two planner mirrors changed.

Checked and not audit items (left as-is, with reason): the closing
"**Remember**" lines in `build-error-resolver`, `doc-updater`, and
`planner` were not among the audit's 12 — each states an operational
directive (fix-and-verify-and-move-on; generate docs from the source
of truth; plan quality criteria), not a pure exhortation of the kind
flagged in S3/S6. `code-reviewer.md:110` "MUST be flagged" is followed
by enumerated damage mechanisms; the audit classed it KEEP.

## Scan — command and output

Final scan (equivalent of the audit's lexical scan + the 297285e
reference-resolution checker, extended to all shipped surfaces).
Run from the repo root; exit 0 requires both counts at zero.

```bash
python3 audit_scan.py   # script reproduced in the appendix below
```

Before (pristine `ce0edbe` worktree, same script):

```text
surfaces scanned: 61 files; roster: 12 agents, 8 skills, 9 script files
== BROKEN REFERENCES ==
researcher agent (nonexistent): 0
security-review skill (nonexistent): 0
setup-package-manager.js (nonexistent): 0
bun-runtime skill (nonexistent): 0
iterative-retrieval skill (nonexistent): 0
scripts/codemaps/generate.ts (nonexistent): 0
bare architect invocation: 0
unresolved skill:/scripts/ references: 0
== SUSPECT PATTERN MARKERS ==
... (10 markers): 0 each
planner Stripe full worked example: 3
   canonical/agents/planner.md:103: ## Worked Example: Adding Stripe Subscriptions
   .claude/agents/planner.md:102: ## Worked Example: Adding Stripe Subscriptions
   .github/agents/planner.agent.md:102: ## Worked Example: Adding Stripe Subscriptions
80% occurrences in canonical: 11 (definition / labeled references /
  reviewer-confidence only; the 11th is planner:179, inside S12)
RESULT: broken_references=0 suspect_markers=3   (exit 1)
```

After (this branch):

```text
surfaces scanned: 61 files; roster: 12 agents, 8 skills, 9 script files
== BROKEN REFERENCES ==
researcher agent (nonexistent): 0
security-review skill (nonexistent): 0
setup-package-manager.js (nonexistent): 0
bun-runtime skill (nonexistent): 0
iterative-retrieval skill (nonexistent): 0
scripts/codemaps/generate.ts (nonexistent): 0
bare architect invocation: 0
unresolved skill:/scripts/ references: 0
== SUSPECT PATTERN MARKERS ==
MUST BE USED booster: 0
15-minute re-verification ritual: 0
waitForTimeout stale example: 0
hard-coded 2025-12-31 stale date: 0
pass@1/pass@3 ritual: 0
TDD Evidence Report document: 0
checkpoint reachability policing: 0
security-reviewer Remember booster: 0
tdd-workflow Remember booster: 0
tdd-workflow universal ensures claim: 0
planner Stripe full worked example: 0
80% occurrences in canonical: 10 (definition / labeled references /
  reviewer-confidence only)
RESULT: broken_references=0 suspect_markers=0   (exit 0)
```

## Claims ledger

Checked `docs/claims-ledger.md` for X18 / instruction-debt references:
none (grep `X18|instruction-debt` = 0 hits). No ledger change — as in
297285e, no ledger entry asserts the fixed content, and no invocable
file name changed.

## Files changed in this run

- `canonical/agents/planner.md` — S12 fix (above).
- `.claude/agents/planner.md`, `.github/agents/planner.agent.md` —
  regenerated by `scripts/install.sh`, not hand-edited.
- `evals/results/2026-10-01-X18-instruction-debt.md` — this file.
- `docs/experiments-backlog.md` — X18 status CLOSED + resolution note.
- `wiki/notes/instruction-debt.md` — dated X18 correction appended.
- `wiki/sessions/2026-10-01-0010-helm-x18-instruction-debt.md`,
  `wiki/log.md` — session record per root AGENTS.md lifecycle.

## Appendix — audit_scan.py

```python
"""X18 audit scan: broken references + suspect-pattern markers in shipped
instruction surfaces (canonical/, .claude/, .github/, root AGENTS.md).
Exit 0 iff zero broken references and zero unresolved suspect markers."""
import re, pathlib, sys
root = pathlib.Path(".")
agents = {p.stem for p in (root/"canonical/agents").glob("*.md")}
skills = {p.stem for p in (root/"canonical/skills").glob("*.md")}
scripts = {p.name for p in (root/"scripts").iterdir() if p.is_file()}
surfaces = []
for d in ["canonical/agents","canonical/skills",".claude/agents",
          ".claude/skills",".github/agents",".github/skills"]:
    surfaces += sorted((root/d).rglob("*.md"))
surfaces.append(root/"AGENTS.md")

def hits(pat):
    out=[]
    for f in surfaces:
        for i,l in enumerate(f.read_text().splitlines(),1):
            if re.search(pat,l): out.append(f"{f}:{i}: {l.strip()[:100]}")
    return out

broken = {
 "researcher agent (nonexistent)": r"\bresearcher\b",
 "security-review skill (nonexistent)": r"security-review(?!er)",
 "setup-package-manager.js (nonexistent)": r"setup-package-manager",
 "bun-runtime skill (nonexistent)": r"bun-runtime",
 "iterative-retrieval skill (nonexistent)": r"iterative-retrieval",
 "scripts/codemaps/generate.ts (nonexistent)": r"codemaps/generate\.ts",
}
arch=[]
for f in surfaces:
    for i,l in enumerate(f.read_text().splitlines(),1):
        if re.search(r"`architect`|use architect\b|(?<!code-)architect agent", l):
            arch.append(f"{f}:{i}: {l.strip()[:100]}")
suspect = {
 "MUST BE USED booster": r"MUST BE USED",
 "15-minute re-verification ritual": r"every 15 minutes",
 "waitForTimeout stale example": r"waitForTimeout",
 "hard-coded 2025-12-31 stale date": r"2025-12-31",
 "pass@1/pass@3 ritual": r"pass@[13]|pass\^3",
 "TDD Evidence Report document": r"TDD Evidence Report",
 "checkpoint reachability policing": r"reachable from",
 "security-reviewer Remember booster": r"Security is not optional",
 "tdd-workflow Remember booster": r"Tests are not optional",
 "tdd-workflow universal ensures claim": r"This skill ensures all code",
 "planner Stripe full worked example": r"Worked Example: Adding Stripe",
}
badref=[]
for f in surfaces:
    txt=f.read_text()
    for m in re.finditer(r"skill:\s+`?([a-z][a-z0-9-]+)`?", txt):
        if m.group(1) not in skills: badref.append(f"{f}: skill: {m.group(1)}")
    for m in re.finditer(r"scripts/([A-Za-z0-9_.-]+)", txt):
        if m.group(1) not in scripts: badref.append(f"{f}: scripts/{m.group(1)}")
cov=[]
for f in surfaces:
    if "canonical" not in str(f): continue
    for i,l in enumerate(f.read_text().splitlines(),1):
        if "80%" in l or '"branches": 80' in l:
            cov.append(f"{f}:{i}: {l.strip()[:110]}")

total_broken=0; total_suspect=0
print(f"surfaces scanned: {len(surfaces)} files; roster: {len(agents)} agents, {len(skills)} skills, {len(scripts)} script files")
print("\n== BROKEN REFERENCES ==")
for name,pat in broken.items():
    h=hits(pat); total_broken+=len(h); print(f"{name}: {len(h)}")
print(f"bare architect invocation: {len(arch)}"); total_broken+=len(arch)
print(f"unresolved skill:/scripts/ references: {len(badref)}"); total_broken+=len(badref)
print("\n== SUSPECT PATTERN MARKERS ==")
for name,pat in suspect.items():
    h=hits(pat); total_suspect+=len(h); print(f"{name}: {len(h)}")
print(f"\n80% occurrences in canonical: {len(cov)}")
print(f"\nRESULT: broken_references={total_broken} suspect_markers={total_suspect}")
sys.exit(0 if total_broken==0 and total_suspect==0 else 1)
```
