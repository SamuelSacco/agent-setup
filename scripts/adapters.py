#!/usr/bin/env python3
"""Adapters: canonical/ definitions -> each tool's native layout.

One install, both tools. Edit canonical/, re-run scripts/install.sh.
Generated files are overwritten; never edit them by hand.

Format notes (verify against live tools — see evals/):
- Claude Code skills:  .claude/skills/<name>/SKILL.md  (frontmatter: name, description)
- Claude Code agents:  .claude/agents/<name>.md       (frontmatter: name, description, model, tools)
- Claude Code MCP:     .mcp.json                       ({"mcpServers": {...}})
- Claude Code hooks:   .claude/settings.json           (hooks.PostToolUseFailure —
  canonical `tool_failure` fires there, PROVEN E4; PostToolUse is success-only)
- Copilot skills:      .github/skills/<name>/SKILL.md  (also discovers .claude/skills)
- Copilot agents:      .github/agents/<name>.agent.md
- Copilot MCP:         .github/mcp.json                ({"servers": {...}})
- Copilot hooks:       .github/hooks/*.json
"""
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CANON = ROOT / "canonical"
CLAUDE = ROOT / ".claude"
COPILOT_GH = ROOT / ".github"

MODEL_MAP = {
    "strong-reasoning": None,  # None = tool default; override per tool below
}


def parse_frontmatter(text: str):
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    if not m:
        return {}, text
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            v = v.strip()
            if v.startswith("[") and v.endswith("]"):
                v = [x.strip() for x in v[1:-1].split(",") if x.strip()]
            fm[k.strip()] = v
    return fm, m.group(2).strip()


def fm_block(fm: dict) -> str:
    lines = ["---"]
    for k, v in fm.items():
        if isinstance(v, list):
            v = "[" + ", ".join(v) + "]"
        lines.append(f"{k}: {v}")
    lines.append("---")
    return "\n".join(lines)


# ---------------------------------------------------------------- skills
def install_skills():
    for src in sorted((CANON / "skills").glob("*.md")):
        fm, body = parse_frontmatter(src.read_text())
        name = fm.get("name", src.stem)
        out_fm = {"name": name, "description": fm.get("description", "")}
        content = f"{fm_block(out_fm)}\n\n{body}\n"
        for base in (CLAUDE / "skills", COPILOT_GH / "skills"):
            dest = base / name / "SKILL.md"
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(content)
        print(f"skill   {name} -> claude + copilot")


# ---------------------------------------------------------------- agents
def install_agents():
    for src in sorted((CANON / "agents").glob("*.md")):
        fm, body = parse_frontmatter(src.read_text())
        name = fm.get("name", src.stem)
        # Claude Code subagent
        c_fm = {"name": name, "description": fm.get("description", "")}
        dest = CLAUDE / "agents" / f"{name}.md"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(f"{fm_block(c_fm)}\n\n{body}\n")
        # Copilot custom agent
        p_fm = {"name": name, "description": fm.get("description", "")}
        dest = COPILOT_GH / "agents" / f"{name}.agent.md"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(f"{fm_block(p_fm)}\n\n{body}\n")
        print(f"agent   {name} -> claude + copilot")


# ---------------------------------------------------------------- mcp
def install_mcp():
    servers = {}
    for src in sorted((CANON / "mcp").glob("*.json")):
        d = json.loads(src.read_text())
        servers[d["name"]] = {
            "command": d["command"],
            "args": d.get("args", []),
            "env": d.get("env", {}),
        }
    # Claude Code: .mcp.json {"mcpServers": {...}}
    (ROOT / ".mcp.json").write_text(json.dumps({"mcpServers": servers}, indent=2) + "\n")
    # Copilot: .github/mcp.json {"servers": {...}}
    COPILOT_GH.mkdir(parents=True, exist_ok=True)
    (COPILOT_GH / "mcp.json").write_text(json.dumps({"servers": servers}, indent=2) + "\n")
    for name in servers:
        print(f"mcp     {name} -> claude + copilot")


# ---------------------------------------------------------------- hooks
def install_hooks():
    settings_hooks = {}
    for src in sorted((CANON / "hooks").glob("*.json")):
        d = json.loads(src.read_text())
        cmd = d["action"]["command"]
        # Claude Code: canonical `tool_failure` maps to PostToolUseFailure
        # (PROVEN E4 2026-09-30: PostToolUse fires only on success and would
        # journal every successful call as a "failure").
        settings_hooks.setdefault("PostToolUseFailure", []).append(
            {"matcher": "*", "hooks": [{"type": "command", "command": cmd}]}
        )
        # Copilot: native hook file under .github/hooks/ (translated, NOT a
        # verbatim copy — public contract is the version:1 envelope with
        # camelCase events and a `bash` command field). REFUTED on the
        # installed CLI v1.0.89 (E4 2026-09-30): the binary contains no
        # postToolUseFailure/sessionStart hook loader and no events fired.
        # Kept so the adapter is correct the day the CLI ships hook support.
        hdir = COPILOT_GH / "hooks"
        hdir.mkdir(parents=True, exist_ok=True)
        native = {
            "version": 1,
            "hooks": {
                "postToolUseFailure": [
                    {"type": "command", "bash": cmd, "timeoutSec": 10}
                ]
            },
        }
        (hdir / f"{d['name']}.json").write_text(json.dumps(native, indent=2) + "\n")
        print(f"hook    {d['name']} -> claude + copilot")
    CLAUDE.mkdir(parents=True, exist_ok=True)
    settings_path = CLAUDE / "settings.json"
    settings = {}
    if settings_path.exists():
        try:
            settings = json.loads(settings_path.read_text())
        except json.JSONDecodeError:
            settings = {}
    settings["hooks"] = settings_hooks
    settings_path.write_text(json.dumps(settings, indent=2) + "\n")


def main():
    install_skills()
    install_agents()
    install_mcp()
    install_hooks()
    print("\nAdapters written. Discovery by each tool is UNVERIFIED until an")
    print("authenticated run lists the capability (see evals/).")


if __name__ == "__main__":
    sys.exit(main())
