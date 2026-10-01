# X13 follow-up Q15 — MCP isolation: is serialized workspace-MCP startup the binding mechanism?

Date: 2026-10-01. Preregistration: `evals/results/2026-10-01-X13-followup-prereg.md`
(committed and pushed BEFORE any run, 7d75979). Parent: X13
(`evals/results/2026-10-01-X13-agent-warmcache.md`). Ledger claim: S15.
Branch `lab/x13-mcp-isolation` off `e181f61` per tasking.

## Design

Agent: `planner` (cleanest X13 serialization signature). Two arms, identical
except one variable — `.github/mcp.json` present (byte-identical to X13's,
sha256 `1ff95bb27dc9aee6babc3df04ca2363cc3820b463eca4dade559c8d228a1a54c`)
vs removed (the "X17 configuration"). Each arm ran under a FRESH copy of an
empty scratch HOME — no `~/.copilot/mcp-config.json` (the W1 user-scope
install), no other copilot state; the workspace file is the only MCP source.
Held constant: CLI 1.0.90, BYOK Anthropic (`COPILOT_PROVIDER_TYPE=anthropic`,
`claude-haiku-4-5-20251001`), `COPILOT_ALLOW_ALL=true`,
`--output-format json --allow-all-tools --allow-all-paths`, `--agent planner`,
300 s timeout, X13's planner prompt verbatim. npx cache shared and warm
(real `~/.npm`, 1.2G) via explicit `NPM_CONFIG_CACHE`. Order: `with`, then
`without`. Trees differ only in `.github/mcp.json` (`diff -r` verified).

Protocol deviation (recorded, not hidden): the first `with` run used a
runner that overrode `PATH` without the ambient entries, so `npx` was
unresolvable; all 5 workspace servers failed instantly
("failed to spawn MCP server process"), `mcp_servers_loaded` fired at ~14 s
session time, run completed in 31 s with both checks passing. That run is
kept as artifact (`runs/with-nopathbug.*`) — it shows fast MCP failure does
not stall the path — and the `with` arm was re-run with the corrected runner
(ambient PATH preserved). Both `with` runs are reported; the verdict rests on
the corrected runs.

## Per-arm timeline

| Arm | Config | Wall | Exit | MCP trace | mcp_servers_loaded | First model call | Result |
|---|---|---|---|---|---|---|---|
| `with` (corrected) | `.github/mcp.json` present, scratch HOME, CLI 1.0.90 | 41 s | 0 | all 5 workspace servers **connected** (no lifecycle failures; no per-server pending/fail events in trace — one `mcp_servers_loaded`) | 04:47:26.175Z (~1 s after first trace event; servers all `connected`, `source: workspace`) | 04:47:26.369Z (model.call_start) → finished 04:47:32.437Z | marker PASS (`COPPER-FALCON-73 CONFIRMED`), persona PASS (Stripe + subscription), 0 tool calls |
| `without` | `.github/mcp.json` removed, scratch HOME, CLI 1.0.90 | 22 s | 0 | no MCP servers defined | 04:47:53.530Z (`[]` — empty server list) | 04:47:53.941Z → result 04:48:06.048Z | Part 1 answered `COPPER-FALCON-73` (codename present, model dropped the `CONFIRMED` suffix in the response body), Part 2 PASS (Stripe Subscription Billing / Stripe), 0 tool calls |
| `with` (nopathbug, artifact) | mcp.json present, npx unresolvable | 31 s | 0 | 5 servers pending→failed instantly, serialized-but-instant ("failed to spawn") | ~14 s session | 1 model call, finished ~21 s | both checks PASS, 0 tool calls |

No arm shows the X13 stall signature: no 60 s lifecycle failures, no
serialized 65 s server starts, no missing `mcp_servers_loaded`, no zero-model-call
kill. The `with` arm — the exact X13 configuration (agent, task, mcp.json,
warm cache) minus only the real HOME and CLI 1.0.89→1.0.90 — completes in
41 s with all five servers connected.

## Verdict

**REFUTED** — under the pre-registered rule: the `with`-file arm completes
fine (exit 0, 41 s, marker + persona pass), so the X13 result does not
reproduce. The emitted `.github/mcp.json`'s presence alone does not trigger
the `--agent` stall in this environment (scratch HOME, no user-scope MCP
config, CLI 1.0.90, warm npx cache).

Scope narrowing (what this does and does not establish):

- It does NOT show serialization is harmless when servers actually fail:
  the 60 s lifecycle failures that X13's mechanism fed on did not occur in
  either arm — all 5 servers connected in ~26 s. The trigger of those
  failures is unlocated (candidates: CLI 1.0.89 vs 1.0.90, real-HOME
  session-store state, or the user-scope `mcp-config.json` duplicating the
  same 5 servers and contending — the real HOME carried both scopes).
- It DOES isolate the workspace file as non-binding: with the file as the
  only MCP source, startup was parallel/fast and the run completed.
- Incidental, scoped to CLI 1.0.90: the S24 claim (workspace MCP scope dead
  on 1.0.89) does not hold here — the `with` arm loaded all 5 servers with
  `source: workspace` from a scratch HOME. S24 stays as recorded for 1.0.89;
  workspace scope works on 1.0.90.

Consequence for S15: the X13 amendment stands as an environment-bound
observation (real HOME + 1.0.89 + user-scope duplication); the mechanism is
not "the emitted `.github/mcp.json` alone." Ledger amended with a dated note;
history not rewritten.

## Spend

3 Copilot BYOK runs (with-nopathbug, with, without). Token totals not printed
in `--output-format json` mode (`premiumRequests: 0` on all). Estimate per run
from the measured baseline (~15–25k input, <1k output) ≈ $0.02–0.03 converted
→ **total ≈ $0.08**, under the $1 cap.

## Artifacts

Runner + raw traces: `~/workspace/q15-x13-scratch/` (`run.sh`,
`runs/{with,without,with-nopathbug}.{jsonl,stderr}`, per-arm HOME snapshots
`home-with/`, `home-without/` created from the empty `home-template/`;
trees `tree-with/`, `tree-without/`).
