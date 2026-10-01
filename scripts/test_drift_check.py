#!/usr/bin/env python3
"""Self-test for scripts/drift_check.py (Q8).

Builds scratch fixtures in a temp dir under the workspace (the repo's
parent dir), plants one fault per check, and asserts:

  (i)   collisions: a skill name at both global and project scope
        exits 1 and names the plant; disjoint scopes exit 0.
  (ii)  secrets: a fake secret in a text file exits 1, names
        file:line, and never prints the full secret (redaction);
        the same file listed in .drift-allow exits 0.
  (iii) pins: a tampered copy of a pinned skill exits 1 and names
        the skill; an @latest MCP spec and a bare unpinned MCP spec
        each exit 1; a correct pin + exact-pinned MCP spec exit 0.
  (iv)  `all` against the real repo tree exits 0.

Prints PASS/FAIL per case; exits nonzero on any failure. Stdlib only.
Scratch fixtures are removed on exit.
"""
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DRIFT = REPO / "scripts" / "drift_check.py"
FAKE_ANTHROPIC = "sk-ant-" + "api03-" + "FAKE0" * 6  # assembled: no literal in source
RESULTS = []


def run(*argv):
    p = subprocess.run(
        [sys.executable, str(DRIFT), *argv],
        capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def record(name, ok, detail=""):
    RESULTS.append((name, ok))
    print(f"{'PASS' if ok else 'FAIL'} {name}" + (f" — {detail}" if detail and not ok else ""))


def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def main() -> int:
    scratch = Path(tempfile.mkdtemp(prefix="drift-test-", dir=str(REPO.parent)))
    try:
        # ---- (i) collisions -------------------------------------------
        home = scratch / "home"
        proj = scratch / "proj"
        write(home / ".agents/skills/planted-skill/SKILL.md", "# global\n")
        write(home / ".claude/skills/other-skill/SKILL.md", "# global\n")
        write(proj / ".claude/skills/planted-skill/SKILL.md", "# project\n")
        write(proj / ".agents/skills/proj-only/SKILL.md", "# project\n")
        rc, out = run("collisions", "--home", str(home), "--project", str(proj))
        record("collisions: planted name at both scopes exits 1 and is named",
               rc == 1 and "planted-skill" in out, f"rc={rc} out={out!r}")

        home2 = scratch / "home2"
        proj2 = scratch / "proj2"
        write(home2 / ".agents/skills/alpha/SKILL.md", "# g\n")
        write(proj2 / ".agents/skills/beta/SKILL.md", "# p\n")
        rc, out = run("collisions", "--home", str(home2), "--project", str(proj2))
        record("collisions: disjoint scopes exit 0", rc == 0, f"rc={rc} out={out!r}")

        # ---- (ii) secrets ---------------------------------------------
        sroot = scratch / "secrets-root"
        write(sroot / "config.txt",
              f"endpoint = https://example.invalid\nkey = {FAKE_ANTHROPIC}\n")
        rc, out = run("secrets", "--root", str(sroot))
        record("secrets: planted fake secret exits 1 with file:line",
               rc == 1 and "config.txt:2" in out, f"rc={rc} out={out!r}")
        record("secrets: full secret never printed (redaction)",
               FAKE_ANTHROPIC not in out, f"out={out!r}")

        write(sroot / ".drift-allow", "config.txt\n")
        rc, out = run("secrets", "--root", str(sroot))
        record("secrets: allowlisted file exits 0", rc == 0, f"rc={rc} out={out!r}")

        sroot2 = scratch / "secrets-clean"
        write(sroot2 / "notes.md", "# notes\nnothing sensitive here\n")
        rc, out = run("secrets", "--root", str(sroot2))
        record("secrets: clean fixture exits 0", rc == 0, f"rc={rc} out={out!r}")

        sroot3 = scratch / "secrets-assignment"
        planted_value = "Zx9Q" + "w8Er7Ty6" + "Ui5Op4As" + "3Df2Gh1J" + "k0Lz"
        write(sroot3 / "env.txt", f'API_TOKEN = "{planted_value}"\n')
        rc, out = run("secrets", "--root", str(sroot3))
        record("secrets: high-entropy KEY/TOKEN assignment exits 1 with file:line",
               rc == 1 and "env.txt:1" in out and planted_value not in out,
               f"rc={rc} out={out!r}")

        # ---- (iii) pins ------------------------------------------------
        proot = scratch / "pins-root"
        content = b"# demo skill\nbody v1\n"
        write(proot / "canonical/skills/demo.md", content.decode())
        pins = {"demo": {"sha256": hashlib.sha256(content).hexdigest(),
                         "source": "fixture", "imported": "2026-10-01",
                         "audit_warnings": []}}
        write(proot / "canonical/skill-pins.json", json.dumps(pins, indent=2))
        write(proot / "canonical/mcp/good.json", json.dumps({
            "name": "good", "command": "npx",
            "args": ["-y", "@example/server@1.2.3"]}))
        rc, out = run("pins", "--root", str(proot))
        record("pins: correct pin + exact MCP pin exit 0",
               rc == 0, f"rc={rc} out={out!r}")

        write(proot / "canonical/skills/demo.md", "# demo skill\nTAMPERED\n")
        rc, out = run("pins", "--root", str(proot))
        record("pins: tampered pinned skill exits 1 and is named",
               rc == 1 and "demo" in out, f"rc={rc} out={out!r}")

        proot2 = scratch / "pins-unpinned"
        write(proot2 / "canonical/mcp/badlatest.json", json.dumps({
            "name": "badlatest", "command": "npx",
            "args": ["-y", "@example/server@latest"]}))
        write(proot2 / "canonical/mcp/badbare.json", json.dumps({
            "name": "badbare", "command": "npx",
            "args": ["-y", "@example/bare"]}))
        rc, out = run("pins", "--root", str(proot2))
        record("pins: @latest and bare unpinned MCP specs exit 1 and are named",
               rc == 1 and "badlatest" in out and "badbare" in out,
               f"rc={rc} out={out!r}")

        # ---- (iv) real repo --------------------------------------------
        rc, out = run("all")
        record("all: real repo tree exits 0", rc == 0, f"rc={rc} out={out!r}")
    finally:
        shutil.rmtree(scratch, ignore_errors=True)

    failed = [n for n, ok in RESULTS if not ok]
    print(f"\n{len(RESULTS) - len(failed)}/{len(RESULTS)} cases PASS")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
