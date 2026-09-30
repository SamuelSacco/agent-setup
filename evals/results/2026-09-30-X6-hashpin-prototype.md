# X6 — Hash-pin + audit-check skill-import prototype

Backlog: `docs/experiments-backlog.md` X6.
Claim under test: packet finding 5 (`docs/phase2-packet-2026-09-30.md`) —
"nobody enforces snapshot + hash-pin + audit-check on import"; status
before this build: **UNBUILT**. This document records a **prototype**:
the smallest real enforcement path, demo-verified. It is not production
enforcement and is not wired into `install.sh`.

## Design (fixed before the demo, 2026-09-30 14:49 EDT)

- Artifact: `scripts/import_skill.py` (single file, stdlib only).
  Why Python: the repo's non-trivial logic already lives in Python
  (`scripts/adapters.py`, `scripts/run_eval.py`); hashing + pattern
  scanning need no new dependencies.
- Subcommands:
  - `import <file.md> [--root DIR] [--force]` — audit, then import into
    `<root>/canonical/skills/<name>.md` and record a pin.
  - `verify [--root DIR]` — recompute every pinned skill's SHA-256 and
    report OK / MISMATCH / MISSING; exit non-zero on any failure.
  - `audit <file.md>` — scan only; exit non-zero if a critical finding.
- Pin store: `<root>/canonical/skill-pins.json` —
  `{name: {sha256, source, imported, audit_warnings[]}}`.
- Skill name comes from frontmatter `name:`; fallback: filename stem.

### Audit policy (stated in advance; the pattern lists live in the script)

- **CRITICAL → refuse import** (exit 3, nothing copied, no pin written):
  - instruction-override phrasing aimed at the agent (e.g. "ignore all
    previous instructions", "disregard … instructions", "new system
    prompt");
  - pipe-to-shell remote execution (`curl … | sh`, `wget … | bash`,
    `| sh` after a download);
  - credential-store references (`~/.ssh`, `id_rsa`, `.aws/credentials`,
    `.env`) combined with a transmit verb (send/upload/post/exfiltrate)
    anywhere in the file.
- **WARNING → import proceeds, finding printed and recorded in the pin:**
  - any `http://` / `https://` URL;
  - shell code fences (```bash / ```sh / ```shell) or `$( … )` command
    substitution;
  - strong agent-directed imperatives ("you must", "always run",
    "never tell the user", "do not mention").
- Existing destination with a *different* hash: refuse (exit 4) unless
  `--force` — an import never silently overwrites a pinned skill.

### Demo protocol (fixed in advance)

Scratch root: `~/workspace/p3/x5x6-scratch/import-demo/` (its own
`canonical/skills/`), so the demo never touches the repo's real canonical
tree.

1. Import a clean skill (`greeting-checklist`) → expect exit 0, file
   present, pin recorded, and the pin's sha256 equal to an independent
   `sha256sum` of the imported file.
2. Import a tampered skill (`helpful-notes`, planted by the author of
   this eval in scratch: instruction-override + `curl | sh` + credential
   exfiltration lines) → expect REFUSED (exit 3), no file imported, no
   pin recorded. If it imports, the prototype fails its decisive test.
3. Modify the imported clean skill in place → `verify` must report
   MISMATCH and exit non-zero. Restore via re-import `--force` →
   `verify` OK. This demonstrates hash-mismatch enforcement after import.

## Demo transcript

Transcript below is verbatim except the tampered fixture's payload
lines, which are redacted to bracketed markers (rule name + line
number carry the evidence). Full unredacted transcript retained
in scratch: `~/workspace/p3/x5x6-scratch/import-demo/transcript.txt`.

```
$ python3 scripts/import_skill.py import /home/hatch/workspace/p3/x5x6-scratch/import-demo/incoming/greeting-checklist.md --root /home/hatch/workspace/p3/x5x6-scratch/import-demo/root
AUDIT greeting-checklist: 0 critical, 0 warning(s)
IMPORTED: greeting-checklist -> canonical/skills/greeting-checklist.md
PINNED:   sha256 2afcdde15cd1e8b4b1303f248783db50d35d3a8a39817e6495ea7fdcb6b501b6
[exit 0]

$ ls /home/hatch/workspace/p3/x5x6-scratch/import-demo/root/canonical/skills/ && cat /home/hatch/workspace/p3/x5x6-scratch/import-demo/root/canonical/skill-pins.json
greeting-checklist.md
{
  "greeting-checklist": {
    "audit_warnings": [],
    "imported": "2026-09-30",
    "sha256": "2afcdde15cd1e8b4b1303f248783db50d35d3a8a39817e6495ea7fdcb6b501b6",
    "source": "/home/hatch/workspace/p3/x5x6-scratch/import-demo/incoming/greeting-checklist.md"
  }
}
[exit 0]

$ sha256sum /home/hatch/workspace/p3/x5x6-scratch/import-demo/root/canonical/skills/greeting-checklist.md
2afcdde15cd1e8b4b1303f248783db50d35d3a8a39817e6495ea7fdcb6b501b6  /home/hatch/workspace/p3/x5x6-scratch/import-demo/root/canonical/skills/greeting-checklist.md
[exit 0]

$ python3 scripts/import_skill.py import /home/hatch/workspace/p3/x5x6-scratch/import-demo/incoming/helpful-notes.md --root /home/hatch/workspace/p3/x5x6-scratch/import-demo/root
AUDIT helpful-notes: 4 critical, 3 warning(s)
  CRITICAL override.ignore-previous (line 8): [planted instruction-override line — redacted]
  CRITICAL exec.pipe-to-shell (line 13): [planted pipe-to-shell line — redacted]
  CRITICAL exec.pipe-to-shell-bare (line 13): [planted pipe-to-shell line — redacted]
  CRITICAL exfil.credential-plus-transmit (line 15): [planted credential-exfiltration line — redacted]
  WARN directive.conceal (line 11): [planted concealment line — redacted]
  WARN net.url (line 13): [planted pipe-to-shell line — redacted]
  WARN net.url (line 16): [planted exfiltration target line — redacted]
REFUSED: helpful-notes has critical audit findings; not imported, no pin written.
[exit 3]

$ ls /home/hatch/workspace/p3/x5x6-scratch/import-demo/root/canonical/skills/ && grep -c helpful-notes /home/hatch/workspace/p3/x5x6-scratch/import-demo/root/canonical/skill-pins.json || echo 'no helpful-notes pin (grep found 0)'
greeting-checklist.md
0
no helpful-notes pin (grep found 0)
[exit 0]

$ echo '<!-- tampered after import -->' >> /home/hatch/workspace/p3/x5x6-scratch/import-demo/root/canonical/skills/greeting-checklist.md
[exit 0]

$ python3 scripts/import_skill.py verify --root /home/hatch/workspace/p3/x5x6-scratch/import-demo/root
MISMATCH  greeting-checklist: current hash != pin 2afcdde15cd1e8b4…
VERIFY: 0/1 pins OK
[exit 1]

$ python3 scripts/import_skill.py import /home/hatch/workspace/p3/x5x6-scratch/import-demo/incoming/greeting-checklist.md --root /home/hatch/workspace/p3/x5x6-scratch/import-demo/root --force
AUDIT greeting-checklist: 0 critical, 0 warning(s)
IMPORTED: greeting-checklist -> canonical/skills/greeting-checklist.md
PINNED:   sha256 2afcdde15cd1e8b4b1303f248783db50d35d3a8a39817e6495ea7fdcb6b501b6
[exit 0]

$ python3 scripts/import_skill.py verify --root /home/hatch/workspace/p3/x5x6-scratch/import-demo/root
OK        greeting-checklist: 2afcdde15cd1e8b4…
VERIFY: 1/1 pins OK
[exit 0]
```

## Verdict

**PROVEN for the prototype as scoped** — the enforcement path works end
to end on the preregistered demo:

1. Clean skill imported (exit 0); pin recorded; the pin's SHA-256 equals
   an independent `sha256sum` of the imported file
   (`2afcdde1…b501b6` in both).
2. Tampered skill **REFUSED** (exit 3): 4 critical findings —
   `override.ignore-previous`, `exec.pipe-to-shell`,
   `exec.pipe-to-shell-bare`, `exfil.credential-plus-transmit` — plus 3
   warnings. No file in `canonical/skills/`, no pin written.
3. Post-import tampering caught: appending one line to the imported file
   made `verify` report MISMATCH (exit 1); re-import with `--force`
   restored the pin and `verify` returned OK (exit 0).

Scope limits, stated plainly: the audit is a pattern list — it catches
the classes it names and will miss novel phrasings; there are no
signatures and no publisher identity; nothing calls this from
`install.sh`. What this closes is the UNBUILT status: snapshot +
hash-pin + audit-check on import now exists as a runnable path with a
passing tamper demo (ledger S19). Hardening it is future work, not a
claim made here.

## Spend

$0 API (local build and demo only).
