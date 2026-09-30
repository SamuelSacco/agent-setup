# BYOK backup — one Anthropic key, both harnesses

Copilot CLI pointed at Anthropic via BYOK env (`COPILOT_PROVIDER_TYPE=anthropic`),
key supplied from the secure vault (stand-in swapped at egress; raw key never
readable here). Prompt: "Reply with exactly: OK".

```
OK

Duration   5s
Tokens     ↑ 14.5k • ↓ 40
```

No **AI Credits** line — GitHub metered nothing. GitHub-hosted runs the same
evening ended with `AI Credits 0.17–0.84`. Claude Code uses the same key via
apiKeyHelper. Model constant, harness the only variable.
Full write-up: `evals/results/2026-09-30-byok-probe.md`.
