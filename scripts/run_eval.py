#!/usr/bin/env python3
"""Packaged eval runner: one task package, one tool, graded from disk.

A task package is a directory under evals/tasks-packaged/<id>/ containing:
  task.json       id, claim under test, source repo + parent/fix commits,
                  grading test files + pytest nodes, model, timeout
  prompt.txt      the prompt handed to the tool ({PYTHON} is substituted
                  with the grading interpreter)
  requirements.txt  grading-environment packages (used only when the runner
                  bootstraps a venv; see --python)

The runner exports the task's PARENT commit (git archive) into a fresh
directory with a fresh single-commit git init, so the run tree contains no
future history and the real fix is unreachable from inside the run. The
tool runs headlessly; grading never trusts the tool's self-report: the
fix commit's test files are overlaid onto the run tree and the grading
nodes are executed by the evaluator. One results file is written to
evals/results/ with per-run cost/turns and a verdict line.

Exit codes: 0 = PASS (grading tests pass), 1 = FAIL, 2 = harness ERROR
(no verdict). Scratch state lives under evals/scratch-run-eval/ (gitignored).
"""
import argparse, io, json, os, re, shutil, subprocess, sys, tarfile, time

DEFAULT_HELPER = os.path.expanduser(
    "~/workspace/skills/anthropic/bin/claude_api_key_helper.py")
DEFAULT_TOOLS = {
    "claude": os.path.expanduser("~/workspace/tools/bin/claude"),
    "copilot": os.path.expanduser("~/workspace/tools/bin/copilot"),
}


def sh(cmd, cwd=None, timeout=None, env=None):
    return subprocess.run(cmd, cwd=cwd, timeout=timeout, env=env,
                          stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, text=True)


def die(msg):
    print(f"run-eval: ERROR: {msg}", file=sys.stderr)
    sys.exit(2)


def resolve_source(task, args, scratch):
    """Return a clean local clone containing parent+fix commits."""
    src = args.source or os.environ.get("EVAL_SOURCE_DIR")
    if not src:
        src = os.path.join(scratch, "cache", f"{task['id']}-src")
        if not os.path.isdir(os.path.join(src, ".git")):
            os.makedirs(os.path.dirname(src), exist_ok=True)
            print(f"run-eval: cloning {task['source']['repo']} -> {src} "
                  f"(one-time, multi-minute for large repos)", flush=True)
            r = sh(["git", "clone", "-q", task["source"]["repo"], src],
                   timeout=1800)
            if r.returncode != 0:
                die(f"source clone failed: {r.stdout[-500:]}")
    if not os.path.isdir(os.path.join(src, ".git")):
        die(f"source is not a git clone: {src}")
    dirty = sh(["git", "-C", src, "status", "--porcelain"]).stdout.strip()
    if dirty:
        die(f"source clone is dirty (grading requires a clean source): "
            f"{dirty[:200]}")
    for label in ("parent", "fix"):
        r = sh(["git", "-C", src, "cat-file", "-t", task["source"][label]])
        if r.stdout.strip() != "commit":
            die(f"source clone lacks {label} commit {task['source'][label]}")
    return src


def resolve_python(task_dir, args, scratch):
    py = args.python or os.environ.get("EVAL_PYTHON")
    if py:
        return py, "explicit (--python / EVAL_PYTHON)"
    probe = sh(["python3", "-c", "import pytest"])
    if probe.returncode == 0:
        return "python3", "system python3 (pytest importable)"
    venv = os.path.join(scratch, "venv")
    if not os.path.exists(os.path.join(venv, "bin", "python")):
        print("run-eval: bootstrapping grading venv (one-time)", flush=True)
        sh(["python3", "-m", "venv", venv], timeout=300)
        req = os.path.join(task_dir, "requirements.txt")
        pkgs = ["pytest", "numpy", "scipy"]
        if os.path.exists(req):
            r = sh([f"{venv}/bin/pip", "install", "-q", "-r", req],
                   timeout=900)
        else:
            r = sh([f"{venv}/bin/pip", "install", "-q", *pkgs], timeout=900)
        if r.returncode != 0:
            die(f"venv bootstrap failed: {r.stdout[-500:]}")
    return f"{venv}/bin/python", "runner-bootstrapped venv (task requirements.txt)"


def api_key_helper():
    h = os.environ.get("CLAUDE_API_KEY_HELPER") or DEFAULT_HELPER
    return h if os.path.exists(h) else None


def setup_run(task, src, rd, args):
    if os.path.exists(rd):
        shutil.rmtree(rd)
    os.makedirs(rd)
    arc = subprocess.run(["git", "-C", src, "archive", task["source"]["parent"]],
                         stdout=subprocess.PIPE, check=True)
    with tarfile.open(fileobj=io.BytesIO(arc.stdout)) as tf:
        tf.extractall(rd)
    sh(["git", "init", "-q"], cwd=rd)
    sh(["git", "add", "-A"], cwd=rd)
    sh(["git", "-c", "user.email=eval@local", "-c", "user.name=eval",
        "commit", "-qm", "baseline"], cwd=rd)
    if args.arm == "orient":
        if not args.orient or not os.path.exists(args.orient):
            die("--arm orient requires --orient <file>")
        shutil.copy(args.orient, os.path.join(rd, "CLAUDE.md"))
    if args.tool == "claude":
        helper = api_key_helper()
        if helper:
            os.makedirs(os.path.join(rd, ".claude"), exist_ok=True)
            with open(os.path.join(rd, ".claude", "settings.json"), "w") as f:
                json.dump({"apiKeyHelper": helper}, f)
        if args.arm == "agent":
            if not args.agent:
                die("--arm agent requires --agent <canonical-agent-name>")
            src_agent = os.path.join(args.repo_root, "canonical", "agents",
                                     f"{args.agent}.md")
            if not os.path.exists(src_agent):
                die(f"canonical agent not found: {src_agent}")
            os.makedirs(os.path.join(rd, ".claude", "agents"), exist_ok=True)
            shutil.copy(src_agent,
                        os.path.join(rd, ".claude", "agents", f"{args.agent}.md"))


def run_tool(task, rd, prompt, args):
    model = args.model or task.get("model", "claude-haiku-4-5-20251001")
    timeout = task.get("timeout_s", 600)
    tool_bin = args.tool_bin or DEFAULT_TOOLS[args.tool]
    if not os.path.exists(tool_bin):
        die(f"tool binary not found: {tool_bin}")
    t0 = time.time()
    timed_out = False
    cost, turns, result, raw = None, None, "", ""
    if args.tool == "claude":
        cmd = [tool_bin, "-p", prompt, "--model", model,
               "--output-format", "json", "--permission-mode", "acceptEdits",
               "--allowedTools", "Write Edit Bash Read Glob Grep"]
        if args.arm == "agent":
            cmd += ["--agent", args.agent]
        try:
            r = sh(cmd, cwd=rd, timeout=timeout)
            raw = r.stdout
        except subprocess.TimeoutExpired as e:
            timed_out = True
            raw = (e.stdout or b"").decode(errors="replace") \
                if isinstance(e.stdout, bytes) else (e.stdout or "")
        try:
            j = json.loads(raw[raw.index("{"):])
            cost = j.get("total_cost_usd")
            if isinstance(cost, (int, float)):
                cost = round(cost, 6)
            turns = j.get("num_turns")
            result = (j.get("result") or "")[:1500]
        except Exception:
            result = f"UNPARSEABLE OUTPUT (timeout={timed_out}): {raw[:500]}"
    else:  # copilot, BYOK Anthropic (same credential/model as claude arm)
        helper = api_key_helper()
        if not helper:
            die("copilot arm needs the Anthropic key helper "
                "(CLAUDE_API_KEY_HELPER) for BYOK; none found")
        key = subprocess.run([helper], stdout=subprocess.PIPE, text=True,
                             check=True).stdout.strip()
        env = dict(os.environ)
        env.update(COPILOT_PROVIDER_TYPE="anthropic",
                   COPILOT_PROVIDER_BASE_URL="https://api.anthropic.com",
                   COPILOT_PROVIDER_MODEL_ID=model,
                   COPILOT_PROVIDER_API_KEY=key,
                   COPILOT_ALLOW_ALL="true")
        try:
            r = sh([tool_bin, "-p", prompt], cwd=rd, timeout=timeout, env=env)
            raw = r.stdout
        except subprocess.TimeoutExpired as e:
            timed_out = True
            raw = (e.stdout or b"").decode(errors="replace") \
                if isinstance(e.stdout, bytes) else (e.stdout or "")
        result = raw[-1500:]
        m_in = re.search(r"↑\s*([\d.]+)\s*([KM]?)", raw)
        m_out = re.search(r"↓\s*([\d.]+)\s*([KM]?)", raw)
        if m_in and m_out:
            def tok(m):
                v = float(m.group(1))
                return v * (1e6 if m.group(2) == "M" else
                            1e3 if m.group(2) == "K" else 1)
            # W3 prereg conversion; footers count cached input at full
            # rate, so this is an upper bound, never a billed figure.
            cost = round(tok(m_in) / 1e6 * 1.0 + tok(m_out) / 1e6 * 5.0, 4)
            turns = "n/a (copilot does not report turns)"
    return dict(cost=cost, turns=turns, result=result, raw=raw,
                wall=round(time.time() - t0), timed_out=timed_out,
                model=model)


def grade(task, src, rd, python):
    for tf_ in task["tests"]["files"]:
        content = subprocess.run(
            ["git", "-C", src, "show", f"{task['source']['fix']}:{tf_}"],
            stdout=subprocess.PIPE, check=True).stdout
        with open(os.path.join(rd, tf_), "wb") as f:
            f.write(content)
    r = sh([python, "-m", "pytest", *task["tests"]["nodes"], "-q"],
           cwd=rd, timeout=600)
    tail = r.stdout.strip().splitlines()[-3:] if r.stdout.strip() else []
    excl = [":!.claude", ":!CLAUDE.md"] + \
           [f":!{x}" for x in task["tests"]["files"]]
    stat_lines = sh(["git", "diff", "--stat", "HEAD", "--", ".", *excl],
                    cwd=rd).stdout.strip().splitlines()
    return r.returncode == 0, tail, (stat_lines[-1] if stat_lines else "")


def main():
    ap = argparse.ArgumentParser(prog="run-eval")
    ap.add_argument("--repo-root", required=True)
    ap.add_argument("--task", required=True, help="task package directory")
    ap.add_argument("--tool", choices=["claude", "copilot"], default="claude")
    ap.add_argument("--arm", choices=["base", "agent", "orient"],
                    default="base")
    ap.add_argument("--agent", help="canonical agent name (--arm agent, claude)")
    ap.add_argument("--orient", help="orientation file (--arm orient)")
    ap.add_argument("--source", help="existing clone with parent+fix commits")
    ap.add_argument("--python", help="grading interpreter")
    ap.add_argument("--model", help="override task model")
    ap.add_argument("--tool-bin", help="override tool binary path")
    args = ap.parse_args()

    task_dir = os.path.abspath(args.task)
    with open(os.path.join(task_dir, "task.json")) as f:
        task = json.load(f)
    scratch = os.path.join(args.repo_root, "evals", "scratch-run-eval")
    os.makedirs(scratch, exist_ok=True)

    src = resolve_source(task, args, scratch)
    python, python_how = resolve_python(task_dir, args, scratch)

    stamp = time.strftime("%Y%m%d-%H%M%S")
    rd = os.path.join(scratch, "runs",
                      f"{task['id']}-{args.tool}-{args.arm}-{stamp}")
    setup_run(task, src, rd, args)
    with open(os.path.join(task_dir, "prompt.txt")) as f:
        prompt = f.read().replace("{PYTHON}", python)

    run = run_tool(task, rd, prompt, args)
    with open(os.path.join(rd, "raw-output.txt"), "w") as f:
        f.write(run["raw"] or "")
    with open(os.path.join(rd, "agent-result.txt"), "w") as f:
        f.write(run["result"] or "")

    if run["timed_out"] or run["cost"] is None and args.tool == "claude" \
            and run["result"].startswith("UNPARSEABLE"):
        verdict, passed = "ERROR", None
    else:
        passed, tail, stat = grade(task, src, rd, python)
        verdict = "PASS" if passed else "FAIL"

    cost_basis = ("metered (tool JSON envelope)" if args.tool == "claude"
                  else "upper-bound estimate (footer tokens at $1/M in, "
                       "$5/M out; cached input at full rate)")
    date = time.strftime("%Y-%m-%d")
    results_name = f"{date}-RUN-{task['id']}-{args.tool}-{args.arm}.md"
    results_path = os.path.join(args.repo_root, "evals", "results",
                                results_name)
    nodes = task["tests"]["nodes"]
    verdict_line = {
        "PASS": f"VERDICT: PASS — grading tests pass on disk "
                f"({len(nodes)}/{len(nodes)} nodes).",
        "FAIL": f"VERDICT: FAIL — grading tests do not pass on disk.",
        "ERROR": "VERDICT: ERROR — harness failure, no verdict on the claim.",
    }[verdict]
    with open(results_path, "w") as f:
        f.write(f"# RUN {task['id']} — {args.tool} / {args.arm}\n\n")
        f.write(f"Date: {date}. Produced by `scripts/run-eval.sh` "
                f"(packaged eval runner).\n\n")
        f.write(f"**{verdict_line}**\n\n")
        f.write(f"Claim under test: {task['claim']}\n\n")
        f.write("| Field | Value |\n|---|---|\n")
        f.write(f"| Task | {task['id']} — {task['title']} |\n")
        f.write(f"| Tool / arm | {args.tool} / {args.arm} |\n")
        f.write(f"| Model | {run['model']} |\n")
        f.write(f"| Success (disk-graded) | "
                f"{'yes' if passed else 'no' if passed is False else 'n/a'} |\n")
        f.write(f"| Turns | {run['turns']} |\n")
        f.write(f"| Cost USD | {run['cost']} — {cost_basis} |\n")
        f.write(f"| Wall s | {run['wall']} |\n")
        f.write(f"| Grading python | {python} ({python_how}) |\n")
        f.write(f"| Source clone | {src} (parent "
                f"{task['source']['parent'][:9]}, fix "
                f"{task['source']['fix'][:9]}) |\n")
        f.write(f"| Run dir | {rd} |\n")
        if verdict != "ERROR":
            f.write(f"| Diff stat (excl. setup + grading tests) | {stat} |\n")
            f.write(f"| Pytest tail | {' | '.join(tail)} |\n")
        f.write("\nAgent's own summary (self-report — not the grade):\n\n")
        f.write(f"```\n{run['result']}\n```\n")
    with open(os.path.join(scratch, "ledger.tsv"), "a") as f:
        f.write("\t".join(str(x) for x in
                          [date, task["id"], args.tool, args.arm, verdict,
                           run["turns"], run["cost"], run["wall"],
                           results_name]) + "\n")
    print(verdict_line)
    print(f"run-eval: results -> evals/results/{results_name}")
    sys.exit(0 if verdict == "PASS" else 1 if verdict == "FAIL" else 2)


if __name__ == "__main__":
    main()
