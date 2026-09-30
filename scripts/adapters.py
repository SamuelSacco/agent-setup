#!/usr/bin/env python3
"""Adapters: canonical/ definitions -> each tool's native layout.

One install, both tools. Edit canonical/, re-run scripts/install.sh.
Generated files are overwritten; never edit them by hand.

Format notes (verify against live tools — see evals/):
- Claude Code skills:  .claude/skills/<name>/SKILL.md  (frontmatter: name, description)
- Claude Code agents:  .claude/agents/<name>.md       (frontmatter: name, description, model, tools)
- Agent tools: canonical `tools_hint` (abstract categories) is translated
  per tool via CLAUDE_TOOL_MAP / COPILOT_TOOL_MAP below and emitted as each
  tool's `tools:` allowlist. Unknown hint -> install fails. Agents with no
  `tools_hint` get no `tools:` line (tool default: all tools).
- Claude Code MCP:     .mcp.json                       ({"mcpServers": {...}})
- Claude Code hooks:   .claude/settings.json           (canonical events map
  via HOOK_EVENT_MAP: `tool_failure` -> PostToolUseFailure, PROVEN E4;
  `session_end` -> SessionEnd, PROVEN headless X5/S18)
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
# tools_hint categories -> per-tool allowlists. Canonical hints are abstract
# (read/search/shell/edit); each tool's `tools:` field takes its own names.
#   Claude Code subagents: tool names (Read, Grep, ...). `search` maps to the
#     two file-search tools only — NOT WebSearch/WebFetch: a code-search hint
#     must not silently grant network access.
#   Copilot custom agents: frontmatter has a `tools` field (default: all) —
#     research: hidden_files/research/2026-09-30-P2-copilot-surface.md §2.
#     Emitted names are the canonical category names, which match Copilot's
#     documented built-in tool categories (read/search/edit/shell); `edit`
#     covers create+edit in that vocabulary, no separate write name exists.
#     Copilot-side *enforcement* of the emitted names is UNVERIFIABLE from
#     this sandbox (CLI not installed here) — probe before claiming parity.
# An agent with no tools_hint gets no `tools:` line (tool default: all).
# An unknown hint aborts the install: a silently dropped restriction is the
# bug this map exists to fix (critique 2026-09-30, Pass 4 HIGH #1).
CLAUDE_TOOL_MAP = {
    "read": ["Read"],
    "search": ["Grep", "Glob"],
    "shell": ["Bash"],
    "edit": ["Write", "Edit"],
}
COPILOT_TOOL_MAP = {
    "read": ["read"],
    "search": ["search"],
    "shell": ["shell"],
    "edit": ["edit"],
}


def translate_tools_hint(hint, tool_map, agent_name):
    if hint is None:
        return None
    tools = []
    for token in hint:
        if token not in tool_map:
            sys.exit(
                f"adapters: agent {agent_name!r} declares unknown tools_hint "
                f"{token!r} (known: {', '.join(sorted(tool_map))}); refusing "
                "to install with a dropped restriction"
            )
        for t in tool_map[token]:
            if t not in tools:
                tools.append(t)
    return tools


def install_agents():
    for src in sorted((CANON / "agents").glob("*.md")):
        fm, body = parse_frontmatter(src.read_text())
        name = fm.get("name", src.stem)
        hint = fm.get("tools_hint")
        # Claude Code subagent
        c_fm = {"name": name, "description": fm.get("description", "")}
        c_tools = translate_tools_hint(hint, CLAUDE_TOOL_MAP, name)
        if c_tools is not None:
            c_fm["tools"] = c_tools
        dest = CLAUDE / "agents" / f"{name}.md"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(f"{fm_block(c_fm)}\n\n{body}\n")
        # Copilot custom agent
        p_fm = {"name": name, "description": fm.get("description", "")}
        p_tools = translate_tools_hint(hint, COPILOT_TOOL_MAP, name)
        if p_tools is not None:
            p_fm["tools"] = p_tools
        dest = COPILOT_GH / "agents" / f"{name}.agent.md"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(f"{fm_block(p_fm)}\n\n{body}\n")
        tools_note = f"tools={c_tools}" if c_tools is not None else "tools=default(all)"
        print(f"agent   {name} -> claude + copilot ({tools_note})")


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
    # Copilot: .github/mcp.json — Copilot CLI requires "mcpServers" (a
    # "servers"-only file is rejected as malformed; P2 W1 evidence
    # 2026-09-30, coordinator-verified). Emit both keys so VS Code-style
    # consumers of "servers" keep working.
    COPILOT_GH.mkdir(parents=True, exist_ok=True)
    (COPILOT_GH / "mcp.json").write_text(json.dumps({"servers": servers, "mcpServers": servers}, indent=2) + "\n")
    for name in servers:
        print(f"mcp     {name} -> claude + copilot")


# ---------------------------------------------------------------- hooks
# Canonical event -> (Claude Code event, Copilot event). Claude:
# `tool_failure` fires on PostToolUseFailure (PROVEN E4 2026-09-30:
# PostToolUse is success-only and would journal every successful call as
# a "failure"); `session_end` fires on SessionEnd (PROVEN headless,
# X5 probe 2026-09-30, ledger S18).
HOOK_EVENT_MAP = {
    "tool_failure": ("PostToolUseFailure", "postToolUseFailure"),
    "session_end": ("SessionEnd", "sessionEnd"),
}


def install_hooks():
    settings_hooks = {}
    for src in sorted((CANON / "hooks").glob("*.json")):
        d = json.loads(src.read_text())
        cmd = d["action"]["command"]
        claude_event, copilot_event = HOOK_EVENT_MAP[d["event"]]
        settings_hooks.setdefault(claude_event, []).append(
            {"matcher": "*", "hooks": [{"type": "command", "command": cmd}]}
        )
        # Copilot: native hook file under .github/hooks/ (translated, NOT a
        # verbatim copy — public contract is the version:1 envelope with
        # camelCase events and a `bash` command field). E4 (2026-09-30,
        # addendum-corrected): on CLI v1.0.89 hooks DO load in a trusted
        # directory (COPILOT_ALLOW_ALL=true) and sessionStart/preToolUse/
        # postToolUse fire; postToolUseFailure did not fire for shell
        # failures because the shell tool reports success on non-zero exit.
        # Failure capture on Copilot therefore needs postToolUse + exit-code
        # parsing (identified, not built); 0/5 failures captured as shipped.
        hdir = COPILOT_GH / "hooks"
        hdir.mkdir(parents=True, exist_ok=True)
        native = {
            "version": 1,
            "hooks": {
                copilot_event: [
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
