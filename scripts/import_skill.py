#!/usr/bin/env python3
"""PROTOTYPE — hash-pin + audit-check enforcement on skill import.

The smallest real version of the packet's forward-looking claim
(docs/phase2-packet-2026-09-30.md, finding 5): nobody enforces
snapshot + hash-pin + audit-check when a skill enters a setup.
This script is that enforcement path, in miniature:

  1. AUDIT   — scan the candidate skill against the policy below.
               CRITICAL findings refuse the import; WARNINGs are
               printed and recorded in the pin.
  2. IMPORT  — copy the skill into canonical/skills/<name>.md.
               Never silently overwrites a pinned file whose hash
               differs (refuses unless --force).
  3. PIN     — record SHA-256 + source + date + audit warnings in
               canonical/skill-pins.json. `verify` re-hashes every
               pinned skill and fails on any mismatch or missing file.

PROTOTYPE: pattern-list audit, single-machine, no signatures, not
wired into scripts/install.sh. It demonstrates the enforcement shape;
it is not production supply-chain security. Evidence + demo:
evals/results/2026-09-30-X6-hashpin-prototype.md (backlog X6, S19).

Usage:
  import_skill.py import <file.md> [--root DIR] [--force]
  import_skill.py verify [--root DIR]
  import_skill.py audit <file.md>

Exit codes: 0 ok · 1 verify failure · 2 usage · 3 refused (critical
audit finding) · 4 refused (would overwrite a pinned skill).
"""
import hashlib
import json
import re
import shutil
import sys
from datetime import date
from pathlib import Path

# ---------------------------------------------------------------- policy
# CRITICAL: refuse import. Patterns are deliberately explicit and
# inspectable — a finding names the rule, line, and matched text.
CRITICAL_PATTERNS = [
    ("override.ignore-previous",
     re.compile(r"ignore\s+(all\s+)?(previous|prior|above)\s+instructions", re.I)),
    ("override.disregard",
     re.compile(r"disregard\s+.{0,40}instructions", re.I)),
    ("override.forget-previous",
     re.compile(r"forget\s+(all\s+)?(previous|prior)\s+instructions", re.I)),
    ("override.new-system-prompt",
     re.compile(r"new\s+system\s+prompt", re.I)),
    ("exec.pipe-to-shell",
     re.compile(r"(curl|wget)\b[^|\n]*\|\s*(sudo\s+)?(ba)?sh\b", re.I)),
    ("exec.pipe-to-shell-bare",
     re.compile(r"\|\s*(sudo\s+)?(ba)?sh\b")),
]
# Credential stores: critical only in combination with a transmit verb
# anywhere in the same file (a skill may legitimately *mention* a path;
# mentioning one while telling the agent to send data out is the attack).
CREDENTIAL_RE = re.compile(r"(~/.ssh|\.ssh/|id_rsa|\.aws/credentials|\.env\b)", re.I)
TRANSMIT_RE = re.compile(r"\b(send|upload|post|transmit|exfiltrate|leak)\b", re.I)

# WARNING: import proceeds; finding is printed and stored in the pin.
WARNING_PATTERNS = [
    ("net.url", re.compile(r"https?://[^\s)]+")),
    ("exec.shell-fence", re.compile(r"```(bash|sh|shell|zsh)\b")),
    ("exec.command-substitution", re.compile(r"\$\(")),
    ("directive.you-must", re.compile(r"\byou\s+must\b", re.I)),
    ("directive.always-run", re.compile(r"\balways\s+run\b", re.I)),
    ("directive.conceal", re.compile(r"\b(never\s+tell|do\s+not\s+(mention|tell))\b", re.I)),
]


def audit_text(text: str):
    """Return (critical, warnings): lists of (rule, line_no, excerpt)."""
    critical, warnings = [], []
    lines = text.splitlines()
    for i, line in enumerate(lines, 1):
        for rule, rx in CRITICAL_PATTERNS:
            m = rx.search(line)
            if m:
                critical.append((rule, i, line.strip()[:100]))
        for rule, rx in WARNING_PATTERNS:
            if rx.search(line):
                warnings.append((rule, i, line.strip()[:100]))
    cred = CREDENTIAL_RE.search(text)
    if cred and TRANSMIT_RE.search(text):
        line_no = text[:cred.start()].count("\n") + 1
        critical.append(("exfil.credential-plus-transmit", line_no,
                         lines[line_no - 1].strip()[:100]))
    return critical, warnings


def skill_name(path: Path, text: str) -> str:
    m = re.search(r"^---\n(.*?)\n---", text, re.S)
    if m:
        n = re.search(r"^name:\s*(.+)$", m.group(1), re.M)
        if n:
            return n.group(1).strip()
    return path.stem


def pins_path(root: Path) -> Path:
    return root / "canonical" / "skill-pins.json"


def load_pins(root: Path) -> dict:
    p = pins_path(root)
    return json.loads(p.read_text()) if p.exists() else {}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def print_findings(kind: str, findings):
    for rule, line_no, excerpt in findings:
        print(f"  {kind} {rule} (line {line_no}): {excerpt}")


def cmd_audit(path: Path) -> int:
    text = path.read_text()
    critical, warnings = audit_text(text)
    print(f"AUDIT {path.name}: {len(critical)} critical, {len(warnings)} warning(s)")
    print_findings("CRITICAL", critical)
    print_findings("WARN", warnings)
    return 3 if critical else 0


def cmd_import(path: Path, root: Path, force: bool) -> int:
    data = path.read_bytes()
    text = data.decode("utf-8")
    name = skill_name(path, text)
    digest = sha256(data)

    critical, warnings = audit_text(text)
    print(f"AUDIT {name}: {len(critical)} critical, {len(warnings)} warning(s)")
    print_findings("CRITICAL", critical)
    print_findings("WARN", warnings)
    if critical:
        print(f"REFUSED: {name} has critical audit findings; not imported, no pin written.")
        return 3

    dest_dir = root / "canonical" / "skills"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / f"{name}.md"
    if dest.exists() and sha256(dest.read_bytes()) != digest and not force:
        print(f"REFUSED: canonical/skills/{name}.md already exists with a "
              f"different hash. Re-run with --force to replace the pin.")
        return 4

    shutil.copyfile(path, dest)
    pins = load_pins(root)
    pins[name] = {
        "sha256": digest,
        "source": str(path),
        "imported": date.today().isoformat(),
        "audit_warnings": [f"{r} (line {n})" for r, n, _ in warnings],
    }
    pins_path(root).write_text(json.dumps(pins, indent=2, sort_keys=True) + "\n")
    print(f"IMPORTED: {name} -> canonical/skills/{name}.md")
    print(f"PINNED:   sha256 {digest}")
    return 0


def cmd_verify(root: Path) -> int:
    pins = load_pins(root)
    if not pins:
        print("VERIFY: no pins recorded.")
        return 0
    bad = 0
    for name, pin in sorted(pins.items()):
        f = root / "canonical" / "skills" / f"{name}.md"
        if not f.exists():
            print(f"MISSING   {name}: pinned file absent")
            bad += 1
        elif sha256(f.read_bytes()) != pin["sha256"]:
            print(f"MISMATCH  {name}: current hash != pin {pin['sha256'][:16]}…")
            bad += 1
        else:
            print(f"OK        {name}: {pin['sha256'][:16]}…")
    print(f"VERIFY: {len(pins) - bad}/{len(pins)} pins OK")
    return 1 if bad else 0


def main(argv) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 2
    cmd, rest = argv[1], argv[2:]
    root = Path(__file__).resolve().parent.parent
    force = "--force" in rest
    if "--root" in rest:
        i = rest.index("--root")
        root = Path(rest[i + 1])
        rest = rest[:i] + rest[i + 2:]
    rest = [a for a in rest if a != "--force"]
    if cmd == "import" and len(rest) == 1:
        return cmd_import(Path(rest[0]), root, force)
    if cmd == "audit" and len(rest) == 1:
        return cmd_audit(Path(rest[0]))
    if cmd == "verify" and not rest:
        return cmd_verify(root)
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
