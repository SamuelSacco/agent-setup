---
id: ecc-ports-invocable
title: Claim — the ECC ports are discoverable and invocable in both tools
type: claim
status: active
created: 2026-09-30
updated: 2026-09-30
verified: 2026-09-30
relates_to: [install-surfaces, v2-roster, specialist-agent-real-code]
sources: []
tags: [evals, ecc, ports, copilot, claude-code]
verdict: PROVEN
evidence: evals/results/2026-09-30-P2-port-verification.md
---

Verified 2026-09-30 (P2 port verification, ledger S14): every capability the
canonical install emits was invoked live in both tools — 12/12 agents (marker
files carrying a token read from disk), 8/8 skills (by name, via each tool's
skill mechanism), 5/5 MCP servers (listed in both; trivial calls answered in
both — playwright only with `--no-sandbox`, an artifact of this root sandbox,
not of the port).

Three operational caveats ride with the verdict. Copilot's `--agent` mode
works for the ported `code-reviewer` (S15, PROVEN — corrected from an
initial REFUTED recorded in error; see the results file) but took ~201 s
for a trivial task, and a second attempt stalled in MCP startup;
delegation via the task tool is the faster, proven path for all 12. Copilot MCP startup fails on a cold npx
cache (parallel cold downloads vs its 60 s handshake cap) — warm the cache or
expect a first-run retry. The github server ships with an empty token by
design: public search works unauthenticated, authenticated operations are
UNVERIFIABLE until a token is set. No adapter-level breakage was found; the
emitted files function as emitted.
