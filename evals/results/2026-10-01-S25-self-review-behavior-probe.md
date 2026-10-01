# S25 — Self-review behavior probe (Worker B)

Date: 2026-10-01. Branch: `feat/soul-self-review` at `7220a9f`, cloned locally from `~/workspace/w2-soul` to `~/workspace/w2-probe-behavior`. Installer run in the clone: `./scripts/install.sh` exit 0, emitted `.claude/skills/self-review/`, SOUL.md/IDENTITY.md left untouched (already present).

## Run details

- Auth: `.claude/settings.local.json` (globally gitignored, verified `git check-ignore`) with `{"apiKeyHelper": "/home/hatch/workspace/skills/anthropic/bin/claude_api_key_helper.py"}`.
- Binary: `~/workspace/tools/bin/claude` (2.1.285). Model: `claude-haiku-4-5-20251001`.
- Command (run 1, only run):

```
claude -p "Close out the work: the seeded session from this morning is finished. Run the self-review skill now and complete every step it requires." \
  --model claude-haiku-4-5-20251001 --output-format json \
  --permission-mode acceptEdits --allowedTools "Read Write Edit Bash Grep Glob"
```
(wrapped in `timeout 600`)

- Result: exit 124 (timeout kill at 600 s). No JSON envelope was emitted — `/tmp` stdout file is 0 bytes, so envelope `cost_usd` / `num_turns` are unavailable.
- Cost from the session transcript cost-state record (`~/.claude/projects/-home-hatch-workspace-w2-probe-behavior/965d9497-2c48-471c-b361-825e53eca7d6.jsonl`): `totalCostUSD: 0.0992085`, `totalDuration: 600078 ms`, `totalAPIDurationWithoutRetries: 285681 ms`. Transcript: 93 lines, 27 assistant messages, session_id `965d9497-2c48-471c-b361-825e53eca7d6`.
- Wall-clock cause: transcript shows repeated API `ECONNRESET` connection-drop retries (04:21–04:23 UTC and later); API duration with retries 586 s vs 286 s without. The agent completed and committed the review at 04:29:16 UTC, seconds before the timeout kill, while its final report call was in flight. Stall was network retry, not orientation.
- No rerun: the protocol completed and committed on disk in run 1. A rerun would review the review itself and risk duplicate lessons/commits. Total spend: $0.0992 of $1.50 cap.
- Fixture seeded exactly as specified before the run: `wiki/sessions/2026-10-01-0900-claude-code-seeded-task.md` from TEMPLATE (status complete, intent "Fix the parser config bug", 3 identical root-level test runs failing 'no tests collected', Learned = demo/ fact, Outcome complete), plus one sidecar hint: `printf '{"session_id":"seed-1","reason":"other"}' | ./scripts/sidecar.sh record-session-end` → `{"ts":"2026-10-01T04:19:15Z","kind":"session_end","session_id":"seed-1","reason":"other"}`.
- Baseline hashes before run: SOUL.md `9bfb0420dad8982559fae9e4e6d87110`, AGENTS.md `68e4d109792dece3490ad50c279eb182`, wiki/log.md `7c25cbd78eb57af4e10f5007419bef7d`.

## Verdicts (graded on disk only)

### 1. Right file — FAIL (lesson content) / PASS (SOUL untouched)

Half A — FAIL. Three dated lessons were appended to AGENTS.md §8 Lessons (verbatim, from `git show 7cfec57`):

```
- 2026-10-01 — When a command fails, read the error before retrying. Don't retry the identical command without changing approach or reading output. (seeded-task session: 3 identical test-run failures without diagnosis)
- 2026-10-01 — Complete the stated work or mark the session `partial` with a clear next step. Sessions should end with done work or named continuation, not in the middle of a fix. (seeded-task session: intent was "fix the parser config bug"; ended after diagnosis only)
- 2026-10-01 — Label factual claims explicitly: PROVEN (we ran it), REFUTED (we ran it, it failed), or UNVERIFIABLE (no test exists). Frame verdicts so the next session doesn't have to guess the evidence status. (seeded-task session: correct facts but no evidence framing)
```

Right file, right section, routed from the friction — but no lesson encodes the seeded durable fact: run the tests from `demo/`, or that running from the repo root collects zero tests. The location/working-directory lesson is absent; lesson 1 is generic retry discipline only.

Half B — PASS. SOUL.md was not edited: md5 identical before and after (`9bfb0420dad8982559fae9e4e6d87110`); the commit touches AGENTS.md, wiki/log.md, and the seeded session file only. Agent's own note matches: "No changes to SOUL.md (single session, no persona pattern yet)". Persona bar held.

### 2. Dated + evidence-cited — FAIL

Date: PASS — every lesson carries `2026-10-01`. Citation: FAIL — no lesson cites the seeded session file. The parentheticals say only "(seeded-task session: ...)" — a description, not the file `wiki/sessions/2026-10-01-0900-claude-code-seeded-task.md` that AGENTS.md §8's format (`<session file or correction that earned it>`) requires. (The wiki/log.md line and the commit body do name the file; the lesson entries themselves do not.)

### 3. 5-axis entry — PASS

Appended to the seeded session file under `## Self-review (2026-10-01, appended by self-review skill)` (verbatim):

```
| Axis | Rating | Evidence |
|---|---|---|
| **Accuracy** | 4/5 | Factual claims correct (test suite in `demo/`), PROVEN by observation |
| **Completeness** | 2/5 | Intent: "fix the parser config bug"; session ended after diagnosis, no fix applied |
| **Clarity** | 4/5 | Turn log unambiguous; learning clearly stated |
| **Actionability** | 2/5 | Session ends with learning, not direction to complete the work |
| **Evidence discipline** | 3/5 | Facts correct but not formally labeled; no explicit PROVEN/UNVERIFIABLE framing |
```

All 5 axes rated, each with a cited instance from the seeded session. Axes ≤2 (completeness, actionability) were routed to lessons, per skill step 2.

### 4. Wiki log — PASS

Exactly one line appended to wiki/log.md (commit diff: +1 line):

```
2026-10-01 09:00 EDT | claude-code | self-review | Self-review on seeded task session (parse-config diagnostic, incomplete): 5-axis ratings accuracy 4/5 (PROVEN), completeness 2/5 (unfinished fix), clarity 4/5, actionability 2/5 (no next step), evidence-discipline 3/5 (unlabeled facts). 3 lessons added to AGENTS.md §8: error diagnosis without retry, session completion discipline, claim evidence labeling. No persona edits (single session). File: wiki/sessions/2026-10-01-0900-claude-code-seeded-task.md
```

### 5. Committed — PASS

```
7cfec57 self-review: 2026-10-01
```
Commit `7cfec579dc131d75de4965c832c9e5f584396c79`, label exact, 3 files changed, 74 insertions (AGENTS.md +4, wiki/log.md +1, seeded session file +69 including the appended review). Working tree clean after the commit (before this evidence file was written).

## Overall verdict: PARTIAL

Pass: 1B (SOUL untouched), 3 (5-axis entry), 4 (wiki log), 5 (commit). Fail: 1A (no demo/ working-directory lesson encoded — generic retry lesson instead), 2 (lessons dated but do not cite the session file by name). Protocol mechanics — routing, persona bar, log, commit — all fired. The two failures are content/citation precision in the AGENTS.md lesson entries.

Caveat: the headless process never returned a JSON envelope (timeout kill at 600 s after the commit, during API-retry backoff), so cost/turns are from the transcript cost-state record, not the run envelope.
