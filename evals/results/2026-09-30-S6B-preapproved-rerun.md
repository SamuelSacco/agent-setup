# S6b pre-approved rerun (Copilot side) — 2026-09-30 ~15:07 ET

Closes the fairness gap in S6b. The pilot ran under default permissions —
the transcript shows every write denied ("Permission denied and could not
request permission from user") — while Claude's S6a pass was scoped "when
writes are pre-approved". This rerun gives Copilot the same conditions.
Same bounded task as the pilot and S6a: state a contract, implement
`TokenBucket` in `ratelimit.py`, write pytest tests (burst / empty-deny /
refill), run them.

## Method

- Fixture: fresh clone of this repo @ 17b3054 (origin/phase-2) in
  `~/workspace/p3/s6b-scratch/e6-copilot-rerun`, `./scripts/install.sh`
  run (emits `.github/agents/backend.agent.md`). Pre-run md5 snapshot of
  all 261 files; `ratelimit.py` / `test_ratelimit.py` absent before.
- Tool: GitHub Copilot CLI 1.0.89 (`~/workspace/tools/bin/copilot`).
- Model: `claude-haiku-4-5-20251001` via BYOK — same provider, model, and
  credential as the pilot and S6a (`COPILOT_PROVIDER_TYPE=anthropic`,
  `COPILOT_PROVIDER_BASE_URL=https://api.anthropic.com`,
  `COPILOT_PROVIDER_MODEL_ID=claude-haiku-4-5-20251001`, key from the
  stored-credential helper; footer carries no AI Credits line).
- Permission mode (the variable under test): `COPILOT_ALLOW_ALL=true`
  plus `--allow-all-tools --allow-all-paths`. Pilot had neither.
- Invocation: `copilot -p "$PROMPT" --agent backend --allow-all-tools
  --allow-all-paths`, cwd = fixture root.
- Prompt (verbatim): "State a contract first. Then implement a
  TokenBucket rate limiter in ratelimit.py in the current directory:
  TokenBucket(capacity, refill_per_sec) with an allow(tokens=1.0) method
  that returns True and consumes the tokens when enough are available,
  and False otherwise; the bucket refills over time up to capacity. Write
  pytest tests in test_ratelimit.py covering: burst up to capacity,
  denial when the bucket is empty, and refill over time. Run the tests
  with pytest and report the results."
- Exit 0, wall 98 s (footer Duration 1m 33s; pilot: 3m 58s). Transcript:
  `2026-09-30-S6B-preapproved-rerun-transcript.txt`.

## Disk evidence (graded from disk, not self-report)

- Tree diff vs pre-run snapshot: only `ratelimit.py` and
  `test_ratelimit.py` added (plus `.pytest_cache/` / `__pycache__/` from
  test runs and a hook append to `wiki/telemetry/events.jsonl`).
- `ratelimit.py` — 1,736 B, md5 `9d0843d9b9d2646e0882012744928bff`:
  `TokenBucket(capacity, refill_per_sec)`, `allow(tokens=1.0) -> bool`,
  monotonic clock, lock.
- `test_ratelimit.py` — 6,092 B, md5 `83d1100ccf58b7344c81ee86648d81cf`:
  20 tests — burst ×3, empty-deny ×3, refill ×5, edge ×6, integration ×3.
- Independent re-run by the grader (fresh venv, pytest 9.1.1):
  **20 passed in 5.23 s, exit 0.**
- Independent contract probe (grader-written, not the agent's tests):
  burst to capacity, deny when empty, refill after 0.25 s, no-refill at
  rate 0 — all behave as specified.
- Zero "Permission denied" lines in the rerun transcript.
- The agent's own loop, for the record: first pytest run 18/20; it then
  edited the two failing tests — both original assertions were wrong
  against the stated contract (fractional-token arithmetic: 0.3×3 spent
  of 1.0 leaves 0.1, so `allow(0.05)` is correctly True; a
  timing-tolerance assertion in the multi-cycle test) — and re-ran to
  20/20. This time the self-report matches the disk.

## Verdict

**PROVEN** (n=1, scoped): Copilot `backend` agent completes the bounded
task when writes are pre-approved.

- vs pilot: REFUTED under default permissions (0 files, fabricated
  "22 passed"). The permission mode was the blocker — the same finding
  as Claude's pilot → S6a rerun. Capability was never the difference.
- vs S6a (Claude, pre-approved): also PROVEN — 13 tests, files on disk,
  $0.0767 metered. Artifacts are comparable (impl 1,736 B vs 1,928 B;
  tests 6,092 B vs 6,233 B). S6 (blind-scored parity grid) remains
  UNVERIFIABLE; this rerun does not change S6.

## Spend

Tokens ↑ 367.3k (327.4k cache-read, 39.8k cache-write) • ↓ 5.2k.
Converted at Haiku list ($1/M input, $5/M output, cached input counted at
full rate per the repo convention — an upper bound, not a billed figure):
**$0.39 converted** of the $2 cap. BYOK bills the Anthropic key directly;
Copilot reports no metered USD.
