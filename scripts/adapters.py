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
- Persona:             canonical/persona/{SOUL,IDENTITY}.md seeds the
  root SOUL.md / IDENTITY.md on first install only. The lived files are
  agent-owned (self-review protocol, AGENTS.md section 8): the
  installer NEVER overwrites them.

Write safety (copilot-critique 2026-09-30 finding #4):
- Every emitted file goes through write_with_backup(): if the existing
  file's content differs, it is first copied to
  <file>.bak-<YYYYMMDD-HHMMSS> next to the original. Identical content
  is not rewritten and creates no backup.
- .claude/settings.json is merged, never replaced: unrelated top-level
  keys and hooks for events canonical does not manage survive an
  install. Malformed (or non-object) settings JSON aborts the install
  BEFORE anything is written: the file is backed up and the error names
  the file and the backup path. It is never silently reset to {}.
"""
import datetime
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


# ---------------------------------------------------------------- write safety
# One timestamp per install run, so every backup from a run shares a suffix.
_BACKUP_STAMP = None


def _backup_stamp() -> str:
    global _BACKUP_STAMP
    if _BACKUP_STAMP is None:
        _BACKUP_STAMP = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    return _BACKUP_STAMP


def backup_file(path: Path) -> Path:
    """Copy `path` to <path>.bak-<YYYYMMDD-HHMMSS> next to the original."""
    dest = path.with_name(f"{path.name}.bak-{_backup_stamp()}")
    n = 1
    while dest.exists():  # same-second collision: keep both backups
        n += 1
        dest = path.with_name(f"{path.name}.bak-{_backup_stamp()}-{n}")
    shutil.copy2(path, dest)
    return dest


def write_with_backup(path: Path, content: str) -> bool:
    """Write `content` to `path`, backing up the prior file first — but only
    when the content actually differs. Identical content is left untouched
    (no rewrite, no backup), so re-running install.sh is a no-op on a
    converged tree. Returns True if the file was (re)written."""
    if path.exists():
        if path.read_text() == content:
            return False
        backup = backup_file(path)
        print(f"backup  {path.relative_to(ROOT)} -> {backup.name}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    return True


def load_existing_settings() -> dict:
    """Return the existing .claude/settings.json as a dict ({} if absent).

    Malformed or non-object JSON is a hard stop, checked before any file
    is written: the offending file is backed up and the install aborts
    naming the file and the backup. The pre-fix behavior silently reset
    a user's settings to {} on a parse error (critique finding #4)."""
    settings_path = CLAUDE / "settings.json"
    if not settings_path.exists():
        return {}
    try:
        data = json.loads(settings_path.read_text())
    except json.JSONDecodeError as e:
        backup = backup_file(settings_path)
        sys.exit(
            f"adapters: {settings_path} is not valid JSON ({e}).\n"
            f"Backed up to {backup}. Fix or remove the file, then re-run install."
        )
    if not isinstance(data, dict):
        backup = backup_file(settings_path)
        sys.exit(
            f"adapters: {settings_path} must contain a JSON object, "
            f"got {type(data).__name__}.\n"
            f"Backed up to {backup}. Fix or remove the file, then re-run install."
        )
    return data


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
            write_with_backup(dest, content)
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
        write_with_backup(dest, f"{fm_block(c_fm)}\n\n{body}\n")
        # Copilot custom agent
        p_fm = {"name": name, "description": fm.get("description", "")}
        p_tools = translate_tools_hint(hint, COPILOT_TOOL_MAP, name)
        if p_tools is not None:
            p_fm["tools"] = p_tools
        dest = COPILOT_GH / "agents" / f"{name}.agent.md"
        write_with_backup(dest, f"{fm_block(p_fm)}\n\n{body}\n")
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
    # MCP configs are fully adapter-owned (no user keys to merge), so a
    # wholesale replace is the correct write here — with the backup that
    # write_with_backup() takes whenever the prior content differs
    # (critique finding #4). .claude/settings.json is the opposite case:
    # it is user-owned and merged instead (see install_hooks).
    # Claude Code: .mcp.json {"mcpServers": {...}}
    write_with_backup(ROOT / ".mcp.json", json.dumps({"mcpServers": servers}, indent=2) + "\n")
    # Copilot: .github/mcp.json — Copilot CLI requires "mcpServers" (a
    # "servers"-only file is rejected as malformed; P2 W1 evidence
    # 2026-09-30, coordinator-verified). Emit both keys so VS Code-style
    # consumers of "servers" keep working.
    write_with_backup(COPILOT_GH / "mcp.json", json.dumps({"servers": servers, "mcpServers": servers}, indent=2) + "\n")
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


def install_hooks(existing_settings: dict):
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
        write_with_backup(hdir / f"{d['name']}.json", json.dumps(native, indent=2) + "\n")
        print(f"hook    {d['name']} -> claude + copilot")
    # settings.json is user-owned, so merge — never replace the file.
    # Unrelated top-level keys survive verbatim; hook events canonical
    # does not manage survive; managed events get the canonical entries.
    # (Malformed settings were already rejected by load_existing_settings()
    # in main(), before anything was written.)
    settings_path = CLAUDE / "settings.json"
    settings = dict(existing_settings)
    existing_hooks = settings.get("hooks")
    if existing_hooks is not None and not isinstance(existing_hooks, dict):
        backup = backup_file(settings_path)
        sys.exit(
            f'adapters: {settings_path} has a "hooks" value that is not a '
            f"JSON object (got {type(existing_hooks).__name__}).\n"
            f"Backed up to {backup}. Fix or remove it, then re-run install."
        )
    merged_hooks = dict(existing_hooks or {})
    merged_hooks.update(settings_hooks)
    settings["hooks"] = merged_hooks
    write_with_backup(settings_path, json.dumps(settings, indent=2) + "\n")


# ---------------------------------------------------------------- persona
def install_persona():
    """Seed root SOUL.md / IDENTITY.md from canonical/persona/ — first
    install only. Persona files are lived documents the agent evolves
    itself (AGENTS.md section 8, `self-review` skill), so unlike every
    other adapter output they are never overwritten and never backed up:
    an existing file is the agent's, full stop."""
    for name in ("SOUL.md", "IDENTITY.md"):
        src = CANON / "persona" / name
        dest = ROOT / name
        if dest.exists():
            print(f"persona {name} exists — agent-owned, left untouched")
        else:
            dest.write_text(src.read_text())
            print(f"persona {name} seeded from canonical/persona/")


def main():
    # Validate the user-owned settings file before writing anything: a
    # malformed one aborts here (with backup), never mid-install.
    existing_settings = load_existing_settings()
    install_persona()
    install_skills()
    install_agents()
    install_mcp()
    install_hooks(existing_settings)
    print("\nAdapters written. Discovery by each tool is UNVERIFIED until an")
    print("authenticated run lists the capability (see evals/).")


if __name__ == "__main__":
    sys.exit(main())
