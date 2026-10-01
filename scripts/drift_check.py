#!/usr/bin/env python3
"""Drift enforcement for the canonical setup (install-scopes §3/§4).

Three checks, stdlib only:

  collisions  Skill names present at BOTH global and project scope.
              Hazard (install-scopes §1a, PROVEN): on a name collision
              Claude runs the global copy, Copilot runs the project
              copy — the same name silently means different content
              per tool. Policy: never the same name in both scopes.

  secrets     Scan a tree for secret-shaped values: Anthropic keys
              (sk-ant-...), GitHub tokens (ghp_/gho_/github_pat_...),
              AWS access keys (AKIA...), PEM private keys, and
              KEY/TOKEN/SECRET assignment lines whose value looks
              high-entropy. Findings print file:line and a short
              redacted prefix — never the full matched secret.
              Allowlist: `.drift-allow` at the scan root, one
              repo-relative path per line (`#` comments allowed).

  pins        (a) Every entry in canonical/skill-pins.json re-hashes
              (SHA-256) to its pinned value — pin loading and hashing
              reuse scripts/import_skill.py (X6). A missing pins file
              means no pins recorded: pass, matching import_skill.py
              `verify`. (b) Every MCP package spec in canonical/mcp/
              *.json (plus package-shaped tokens in
              scripts/adapters.py) carries an exact version pin:
              `@latest`, a range, or a bare unpinned name is flagged.

  all         Run all three against the repo root with the real
              HOME / project defaults. One-line summary per check.
              This is the weekly verify entry point
              (scripts/verify-weekly.sh).

Not wired into scripts/install.sh (follow-up, out of scope for Q8).

Usage:
  drift_check.py collisions [--home DIR] [--project DIR]
  drift_check.py secrets [--root DIR]
  drift_check.py pins [--root DIR]
  drift_check.py all

Exit codes: 0 clean · 1 findings · 2 usage.
"""
import argparse
import hashlib
import json
import math
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MAX_FILE_BYTES = 1024 * 1024  # secrets scan size cap

# ---------------------------------------------------------------- collisions

GLOBAL_DIRS = (".agents/skills", ".claude/skills")
PROJECT_DIRS = (".agents/skills", ".claude/skills")


def skill_names(base: Path, rel_dirs) -> dict:
    """Map skill name -> [paths] under each scope dir below `base`.

    A skill entry is a directory named for the skill, or a flat
    `<name>.md` file. Hidden entries and lock files are not skills.
    """
    found = {}
    for rel in rel_dirs:
        d = base / rel
        if not d.is_dir():
            continue
        for entry in sorted(d.iterdir()):
            if entry.name.startswith("."):
                continue
            if entry.is_dir():
                found.setdefault(entry.name, []).append(str(entry))
            elif entry.is_file() and entry.suffix == ".md":
                found.setdefault(entry.stem, []).append(str(entry))
    return found


def check_collisions(home: Path, project: Path) -> list:
    global_names = skill_names(home, GLOBAL_DIRS)
    project_names = skill_names(project, PROJECT_DIRS)
    findings = []
    for name in sorted(set(global_names) & set(project_names)):
        findings.append(
            f"COLLISION {name}: global {global_names[name]} vs "
            f"project {project_names[name]} — Claude runs the global "
            f"copy, Copilot runs the project copy (install-scopes §1a)"
        )
    return findings


# ---------------------------------------------------------------- secrets

SECRET_PATTERNS = [
    ("anthropic-key", re.compile(r"sk-ant-[A-Za-z0-9_-]{10,}")),
    ("github-token", re.compile(
        r"(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{20,}"
        r"|github_pat_[A-Za-z0-9_]{20,}")),
    ("aws-access-key", re.compile(r"\bAKIA[A-Z0-9]{16}\b")),
    ("private-key", re.compile(r"-----BEGIN (?:[A-Z0-9 ]+ )?PRIVATE KEY-----")),
]
ASSIGNMENT_RE = re.compile(
    r"^\s*(?:export\s+)?[\"']?([A-Za-z_][A-Za-z0-9_]*)[\"']?\s*[:=]\s*"
    r"(?:[\"']([A-Za-z0-9_\-+/=.]{16,})[\"']|([A-Za-z0-9_\-+/=]{16,}))"
)
ASSIGNMENT_KEYWORDS = ("KEY", "TOKEN", "SECRET", "PASSWORD", "PASSWD",
                       "CREDENTIAL")


def is_secret_name(name: str) -> bool:
    """Env-style (SCREAMING_SNAKE) or snake_case names only.

    CamelCase attributes, Python kwargs (`key=`, `tokens=`), and test
    method names are code, not secret assignments — flagging them made
    the scan cry wolf on this repo's own sources.
    """
    if not (re.fullmatch(r"[A-Z][A-Z0-9_]*", name)
            or re.fullmatch(r"[a-z][a-z0-9_]*", name)):
        return False
    upper = name.upper()
    return any(k in upper for k in ASSIGNMENT_KEYWORDS)
PLACEHOLDER_MARKERS = (
    "example", "placeholder", "your-", "your_", "xxx", "changeme",
    "change-me", "redacted", "dummy", "sample", "<", "${", "{{", "...",
    "not-a-real", "fake",
)


def shannon_entropy(value: str) -> float:
    if not value:
        return 0.0
    counts = {}
    for ch in value:
        counts[ch] = counts.get(ch, 0) + 1
    n = len(value)
    return -sum((c / n) * math.log2(c / n) for c in counts.values())


def looks_high_entropy(value: str) -> bool:
    if len(value) < 16:
        return False
    low = value.lower()
    if any(m in low for m in PLACEHOLDER_MARKERS):
        return False
    classes = sum([
        any(c.islower() for c in value),
        any(c.isupper() for c in value),
        any(c.isdigit() for c in value),
        any(not c.isalnum() for c in value),
    ])
    return classes >= 2 and shannon_entropy(value) >= 3.5


def redact(matched: str) -> str:
    """Short prefix only — the full secret is never printed."""
    return matched[:6] + "…[redacted]"


def load_allowlist(root: Path) -> set:
    allow_file = root / ".drift-allow"
    allowed = set()
    if allow_file.is_file():
        for line in allow_file.read_text(errors="ignore").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                allowed.add(line.rstrip("/"))
    return allowed


def is_allowlisted(rel_posix: str, allowed: set) -> bool:
    return any(rel_posix == a or rel_posix.startswith(a + "/") for a in allowed)


def check_secrets(root: Path) -> list:
    findings = []
    allowed = load_allowlist(root)
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        if ".git" in path.relative_to(root).parts:
            continue
        if is_allowlisted(rel, allowed):
            continue
        try:
            if path.stat().st_size > MAX_FILE_BYTES:
                continue
            data = path.read_bytes()
        except OSError:
            continue
        if b"\x00" in data[:8192]:  # binary
            continue
        text = data.decode("utf-8", errors="ignore")
        for line_no, line in enumerate(text.splitlines(), 1):
            hit = False
            for rule, rx in SECRET_PATTERNS:
                m = rx.search(line)
                if m:
                    findings.append(
                        f"{rel}:{line_no}: {rule} {redact(m.group(0))}")
                    hit = True
            if hit:
                continue  # one report per line is enough
            m = ASSIGNMENT_RE.search(line)
            if m and is_secret_name(m.group(1)):
                value = m.group(2) or m.group(3) or ""
                if looks_high_entropy(value):
                    findings.append(
                        f"{rel}:{line_no}: high-entropy-assignment "
                        f"{m.group(1)}={redact(value)}")
    return findings


# ---------------------------------------------------------------- pins

def _import_skill_helpers():
    """Reuse X6 pin logic from scripts/import_skill.py where practical."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    try:
        import import_skill
        return import_skill.load_pins, import_skill.sha256
    except Exception:
        return None, None


def exact_version(spec: str):
    """Return the pinned version if `spec` carries an exact pin, else None."""
    if spec.startswith("@"):
        idx = spec.find("@", 1)
    else:
        idx = spec.find("@")
    if idx < 0:
        return None
    version = spec[idx + 1:]
    if re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?", version):
        return version
    return None


PACKAGE_SHAPE = re.compile(
    r"^(@[A-Za-z0-9._-]+/[A-Za-z0-9._-]+|[A-Za-z0-9._-]+)(@\S+)?$")
# Flags whose following argument is a value, not a package spec.
VALUE_FLAGS = {
    "--browser", "--browser-channel", "--port", "--host",
    "--user-data-dir", "--output", "--config", "--executable-path",
}


def mcp_spec_findings(root: Path) -> list:
    findings = []
    mcp_dir = root / "canonical" / "mcp"
    if mcp_dir.is_dir():
        for src in sorted(mcp_dir.glob("*.json")):
            try:
                spec = json.loads(src.read_text())
            except (OSError, json.JSONDecodeError) as e:
                findings.append(f"MCP {src.name}: unreadable JSON ({e})")
                continue
            name = spec.get("name", src.stem)
            command = spec.get("command", "")
            is_runner = command in ("npx", "pnpx", "bunx")
            positional = 0
            prev = None
            for arg in spec.get("args", []):
                if not isinstance(arg, str):
                    continue
                if arg.startswith("-"):
                    prev = arg
                    continue
                if prev in VALUE_FLAGS:
                    prev = arg
                    continue
                prev = arg
                positional += 1
                if arg.startswith((".", "/", "~")):
                    continue  # path argument, not a package
                if not PACKAGE_SHAPE.match(arg):
                    continue
                if not (arg.startswith("@") or is_runner and positional == 1):
                    continue
                if exact_version(arg) is None:
                    findings.append(
                        f"MCP {name} ({src.name}): package spec {arg!r} "
                        f"has no exact version pin (@latest or bare "
                        f"unpinned names are drift)")
    # Adapter sources: flag any package-shaped token with @latest /
    # no exact pin. adapters.py currently embeds no specs; scanned so
    # a future hardcoded spec cannot drift silently.
    adapters = root / "scripts" / "adapters.py"
    if adapters.is_file():
        token_rx = re.compile(
            r"@[A-Za-z0-9._-]+/[A-Za-z0-9._-]+(?:@[A-Za-z0-9._~^*<>=-]+)?")
        for tok in sorted(set(token_rx.findall(adapters.read_text(
                errors="ignore")))):
            if exact_version(tok) is None:
                findings.append(
                    f"MCP adapters.py: package spec {tok!r} has no "
                    f"exact version pin")
    return findings


def check_pins(root: Path) -> list:
    findings = []
    load_pins, sha256_fn = _import_skill_helpers()
    if load_pins is None:  # fallback: same semantics, local copy
        def load_pins(r):
            p = r / "canonical" / "skill-pins.json"
            return json.loads(p.read_text()) if p.exists() else {}

        def sha256_fn(data):
            return hashlib.sha256(data).hexdigest()
    pins = load_pins(root)
    for name, pin in sorted(pins.items()):
        f = root / "canonical" / "skills" / f"{name}.md"
        if not f.exists():
            findings.append(f"PIN {name}: pinned file missing "
                            f"(canonical/skills/{name}.md)")
        elif sha256_fn(f.read_bytes()) != pin.get("sha256"):
            findings.append(f"PIN {name}: SHA-256 mismatch — file "
                            f"differs from canonical/skill-pins.json")
    findings.extend(mcp_spec_findings(root))
    return findings, len(pins)


# ---------------------------------------------------------------- commands

def cmd_collisions(args) -> int:
    findings = check_collisions(Path(args.home), Path(args.project))
    for f in findings:
        print(f)
    print(f"collisions: {len(findings)} collision(s)")
    return 1 if findings else 0


def cmd_secrets(args) -> int:
    root = Path(args.root)
    findings = check_secrets(root)
    for f in findings:
        print(f)
    print(f"secrets: {len(findings)} finding(s) under {root}")
    return 1 if findings else 0


def cmd_pins(args) -> int:
    root = Path(args.root)
    findings, n_pins = check_pins(root)
    for f in findings:
        print(f)
    if n_pins:
        print(f"pins: {n_pins} skill pin(s) checked, "
              f"{len(findings)} finding(s)")
    else:
        print("pins: no pins recorded in canonical/skill-pins.json "
              "(vacuous pass, matches import_skill.py verify); "
              f"MCP spec check: {len(findings)} finding(s)")
    return 1 if findings else 0


def cmd_all(args) -> int:
    root = REPO_ROOT
    home, project = Path.home(), root
    results = []

    findings = check_collisions(home, project)
    for f in findings:
        print(f)
    results.append(("collisions", findings))
    print(f"collisions: {'FAIL' if findings else 'OK'} "
          f"({len(findings)} collision(s), home={home}, project={project})")

    findings = check_secrets(root)
    for f in findings:
        print(f)
    results.append(("secrets", findings))
    print(f"secrets: {'FAIL' if findings else 'OK'} "
          f"({len(findings)} finding(s), root={root})")

    findings, n_pins = check_pins(root)
    for f in findings:
        print(f)
    results.append(("pins", findings))
    print(f"pins: {'FAIL' if findings else 'OK'} "
          f"({n_pins} skill pin(s), {len(findings)} finding(s), root={root})")

    bad = [name for name, f in results if f]
    print(f"all: {'FAIL — ' + ', '.join(bad) if bad else 'OK — all checks clean'}")
    return 1 if bad else 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="cmd")
    p = sub.add_parser("collisions")
    p.add_argument("--home", default=str(Path.home()))
    p.add_argument("--project", default=str(REPO_ROOT))
    p = sub.add_parser("secrets")
    p.add_argument("--root", default=str(REPO_ROOT))
    p = sub.add_parser("pins")
    p.add_argument("--root", default=str(REPO_ROOT))
    sub.add_parser("all")
    args = parser.parse_args(argv)
    handlers = {"collisions": cmd_collisions, "secrets": cmd_secrets,
                "pins": cmd_pins, "all": cmd_all}
    if args.cmd not in handlers:
        parser.print_help()
        return 2
    return handlers[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
