#!/usr/bin/env python3
"""X8 / E3 runner: one task, one arm, graded from disk.

Usage: run_x8.py <t1|t2|t3|t4|t5> <A|B>
Copies the fixture workspace to evals/scratch-x8/runs/<task>-<arm>/,
applies the arm treatment, runs Claude Code headless (Haiku), then
grades from disk: hidden pytest files (code tasks) or token checks
on ANSWER.md (answer tasks). Appends a row to evals/scratch-x8/ledger.tsv
and prints a one-line JSON summary. Never grades agent self-report.
"""
import json, os, shutil, subprocess, sys, time

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
FIX = os.path.join(ROOT, "evals", "fixtures", "x8-e3")
SCRATCH = os.path.join(ROOT, "evals", "scratch-x8")
CLAUDE = os.path.expanduser("~/workspace/tools/bin/claude")
HELPER = os.path.expanduser("~/workspace/skills/anthropic/bin/claude_api_key_helper.py")
MODEL = "claude-haiku-4-5-20251001"
TIMEOUT = 300

def sh(cmd, cwd=None, timeout=None):
    return subprocess.run(cmd, cwd=cwd, timeout=timeout, stdin=subprocess.DEVNULL,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

def main():
    task, arm = sys.argv[1], sys.argv[2]
    assert task in ("t1","t2","t3","t4","t5") and arm in ("A","B")
    rd = os.path.join(SCRATCH, "runs", f"{task}-{arm}")
    if os.path.exists(rd):
        shutil.rmtree(rd)
    shutil.copytree(os.path.join(FIX, "workspace"), rd,
                    ignore=shutil.ignore_patterns("AGENTS-armA.md","AGENTS-armB.md"))
    # arm treatment
    src_agents = os.path.join(FIX, "workspace", f"AGENTS-arm{arm}.md")
    shutil.copy(src_agents, os.path.join(rd, "AGENTS.md"))
    if arm == "B":
        notes = os.path.join(rd, "wiki", "notes")
        shutil.rmtree(notes); os.makedirs(notes)
        open(os.path.join(notes, ".gitkeep"), "w").close()
    os.makedirs(os.path.join(rd, ".claude"), exist_ok=True)
    with open(os.path.join(rd, ".claude", "settings.json"), "w") as f:
        json.dump({"apiKeyHelper": HELPER}, f)
    sh(["git","init","-q"], cwd=rd)
    sh(["git","add","-A"], cwd=rd)
    sh(["git","-c","user.email=eval@local","-c","user.name=eval","commit","-qm","baseline"], cwd=rd)

    with open(os.path.join(FIX, "prompts", f"{task}.txt")) as f:
        prompt = f.read().strip()
    t0 = time.time()
    timed_out = False
    try:
        r = sh([CLAUDE, "-p", prompt, "--model", MODEL, "--output-format", "json",
                "--permission-mode", "acceptEdits",
                "--allowedTools", "Write Edit Bash Read Glob Grep"], cwd=rd, timeout=TIMEOUT)
        raw = r.stdout
    except subprocess.TimeoutExpired as e:
        timed_out = True
        raw = (e.stdout or b"").decode(errors="replace") if isinstance(e.stdout, bytes) else (e.stdout or "")
    wall = round(time.time() - t0)
    with open(os.path.join(rd, "raw-output.json"), "w") as f:
        f.write(raw or "")
    cost = turns = None; in_tok = total_in = None; result = ""
    try:
        j = json.loads(raw[raw.index("{"):])
        cost = j.get("total_cost_usd"); turns = j.get("num_turns"); result = (j.get("result") or "")[:1500]
        u = j.get("usage") or {}
        in_tok = u.get("input_tokens")
        total_in = (u.get("input_tokens") or 0) + (u.get("cache_creation_input_tokens") or 0) + (u.get("cache_read_input_tokens") or 0)
    except Exception:
        result = f"UNPARSEABLE (timeout={timed_out}): {(raw or '')[:400]}"
    with open(os.path.join(rd, "agent-result.txt"), "w") as f:
        f.write(result)

    # ---- grading from disk ----
    passed = None; violations = None; grade_detail = ""
    if task in ("t1","t2","t4"):
        gt = os.path.join(FIX, "grading", f"test_{task}.py")
        shutil.copy(gt, os.path.join(rd, f"test_grade_{task}.py"))
        # Stdlib grading harness: grading tests are plain assert
        # functions (no pytest fixtures); pip installs are unreliable
        # in this sandbox, so grading must not depend on pytest.
        harness = (
            "import importlib, sys, traceback\n"
            f"m = importlib.import_module('test_grade_{task}')\n"
            "fails = 0; total = 0\n"
            "for name in sorted(dir(m)):\n"
            "    if name.startswith('test_'):\n"
            "        total += 1\n"
            "        try:\n"
            "            getattr(m, name)(); print(f'PASS {name}')\n"
            "        except Exception:\n"
            "            fails += 1; print(f'FAIL {name}'); traceback.print_exc()\n"
            "print(f'{total - fails} passed, {fails} failed')\n"
            "sys.exit(1 if fails else 0)\n"
        )
        with open(os.path.join(rd, "grade_harness.py"), "w") as f:
            f.write(harness)
        gr = sh(["python3","grade_harness.py"], cwd=rd, timeout=120)
        grade_detail = gr.stdout.strip().splitlines()[-1] if gr.stdout.strip() else ""
        import re
        m = re.search(r"(\d+) failed", gr.stdout)
        violations = int(m.group(1)) if m else 0
        if gr.returncode != 0 and violations == 0:
            violations = 1  # import/collection error etc.
        passed = (gr.returncode == 0)
        with open(os.path.join(rd, "grade.txt"), "w") as f:
            f.write(gr.stdout)
    else:
        checks = json.load(open(os.path.join(FIX, "grading", "answer_checks.json")))[task]
        apath = os.path.join(rd, "ANSWER.md")
        text = open(apath, encoding="utf-8", errors="replace").read().lower() if os.path.exists(apath) else ""
        missing = [g for g in checks["required_groups"] if not any(s.lower() in text for s in g)]
        forb = [s for s in checks["forbidden"] if s.lower() in text]
        violations = len(forb)
        passed = bool(text) and not missing and not forb
        grade_detail = f"missing_groups={missing} forbidden_found={forb}"
        with open(os.path.join(rd, "grade.txt"), "w") as f:
            f.write(grade_detail + "\n")

    diff = sh(["git","diff","--stat","HEAD","--",".",":!.claude",":!raw-output.json",":!agent-result.txt",":!grade.txt",":!grade_harness.py",f":!test_grade_{task}.py"], cwd=rd).stdout.strip()
    summary = dict(task=task, arm=arm, passed=passed, turns=turns, cost=cost,
                   input_tokens=in_tok, total_input_tokens=total_in, wall=wall,
                   violations=violations, grade_detail=grade_detail,
                   timed_out=timed_out, diff_stat=diff.splitlines()[-1] if diff else "",
                   run_dir=rd)
    os.makedirs(SCRATCH, exist_ok=True)
    with open(os.path.join(SCRATCH, "ledger.tsv"), "a") as f:
        f.write("\t".join(str(summary[k]) for k in ("task","arm","passed","turns","cost","total_input_tokens","wall","violations")) + "\n")
    print(json.dumps(summary))

if __name__ == "__main__":
    main()
