# X9 / E6 re-run — Copilot arm pre-registration — 2026-10-01 00:35 ET

Registered BEFORE any paid CLI run on this branch. Branch
`wave2c/x9-e6-copilot-arm` off master `e181f61`. Copilot arm only; the
Claude arm runs on a separate branch by a separate worker. Parity (S6)
is decided only when both arms' disk-graded scores exist.

## Protocol — unchanged from E6 as instantiated (pilot + S6a + S6b)

The E6 grid as designed (`evals/tasks/E6-agent-parity.md`: 3 agents ×
blind scoring) was never run; the only task package ever instantiated
is the `backend` / TokenBucket bounded task used by the pilot, the S6a
Claude rerun, and the S6b pre-approved Copilot rerun. X9's decisive
test (backlog): "re-run the E6 protocol with disk grading on both
tools, same task package." This arm re-runs that package unchanged:

- Fixture: fresh clone of this repo @ `e181f61` under
  `~/workspace/w2c-x9-scratch/fixture`, `./scripts/install.sh` run
  (emits `.github/agents/backend.agent.md`). Pre-run md5 snapshot of
  the fixture tree; `ratelimit.py` / `test_ratelimit.py` absent before.
- Tool: GitHub Copilot CLI at `~/workspace/tools/bin/copilot`
  (version recorded at run time; 1.0.89 in prior probes).
- Model: `claude-haiku-4-5-20251001` via BYOK — same provider, model,
  and credential as the pilot, S6a, and S6b (`COPILOT_PROVIDER_TYPE=
  anthropic`, `COPILOT_PROVIDER_BASE_URL=https://api.anthropic.com`,
  key from the stored-credential helper, never written to disk here).
- Permission mode: pre-approved writes, as in S6a/S6b —
  `COPILOT_ALLOW_ALL=true` plus `--allow-all-tools --allow-all-paths`.
  (The pilot's default-permission condition is not re-run: it is
  already REFUTED and audit-scoped as a permission artifact.)
- Invocation: `copilot -p "$PROMPT" --agent backend --allow-all-tools
  --allow-all-paths`, cwd = fixture root, timeout 600 s.
- Prompt (verbatim, identical to S6b): "State a contract first. Then
  implement a TokenBucket rate limiter in ratelimit.py in the current
  directory: TokenBucket(capacity, refill_per_sec) with an
  allow(tokens=1.0) method that returns True and consumes the tokens
  when enough are available, and False otherwise; the bucket refills
  over time up to capacity. Write pytest tests in test_ratelimit.py
  covering: burst up to capacity, denial when the bucket is empty, and
  refill over time. Run the tests with pytest and report the results."
- Runs: 1 planned; at most 2 if the first fails mechanically (crash /
  timeout / zero-token exit). Stop if cumulative converted spend
  would exceed the $1 cap for this arm.

## The one change: grading from disk artifacts only

- Tree diff vs the pre-run md5 snapshot names every file the run added
  or changed. Agent self-report is recorded, never graded.
- Independent grader re-run of the on-disk tests in a fresh venv
  (pytest), exit code + pass count recorded.
- Grader-written contract probe (not the agent's tests): burst to
  capacity, deny when empty, refill after a timed wait, no refill at
  rate 0.
- Rubric score /10 from disk artifacts (E6 axes, weights fixed here):
  correctness 0–4 (contract probe pass = 3, plus grader pytest exit 0
  = 1), test presence/coverage 0–2 (all three required scenarios
  present and passing = 2; partial = 1), convention fit 0–2 (module +
  API exactly as specified, contract stated in the artifact = 2),
  clarity 0–2 (grader read of the two files). Scoring is disk-based,
  not blind — the scorer knows the arm; blindness is impossible
  single-arm and is not claimed.
- Verdicts: arm completion PROVEN only if both files exist on disk,
  grader pytest exits 0, and the contract probe passes. Anything less
  is REFUTED (files present but failing) or UNVERIFIABLE (no run).

## Spend accounting

Copilot BYOK reports tokens, no metered USD and no AI Credits line.
Converted at Haiku list ($1/M input, $5/M output, cached input counted
at full rate per repo convention — an upper bound, not a billed
figure). Cap: $1 converted for this arm. S6b anchor: $0.39 converted.
