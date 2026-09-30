# Same-key both-harnesses probe — 2026-09-30 (~01:07 ET)

Samuel's proposal: point Copilot CLI at the same Anthropic API key Claude Code
uses (BYOK), so the model and account are identical and only the harness
differs.

## Verification

1. Binary check: installed Copilot CLI v1.0.89 (`app.js`) contains
   `COPILOT_PROVIDER_TYPE`, `COPILOT_PROVIDER_BASE_URL`,
   `COPILOT_PROVIDER_API_KEY`, `COPILOT_PROVIDER_MODEL_ID`, and BYOK
   references. Claim is real, not marketing.
2. Live probe: `copilot -p 'Reply with exactly: OK'` with
   `COPILOT_PROVIDER_TYPE=anthropic`,
   `COPILOT_PROVIDER_BASE_URL=https://api.anthropic.com`,
   `COPILOT_PROVIDER_MODEL_ID=claude-haiku-4-5-20251001`, and the stored
   Anthropic credential (via the vault surrogate — the raw key is never
   readable here).
   - Returned `OK`.
   - Footer: `Duration 5s · Tokens ↑ 14.5k ↓ 40` — **no AI Credits line**.
     GitHub-hosted runs earlier tonight showed `AI Credits 0.17`. Billing
     went to Anthropic, not GitHub quota.

## Verdict

**PROVEN.** One Anthropic account/key now drives both harnesses:
Claude Code (apiKeyHelper) and Copilot CLI (BYOK env). Model choice is a
config variable on both sides, so harness effects can be isolated from
model effects.

Side observation for E5/E6: Copilot's harness sent ~14.5k input tokens for
a one-word reply vs ~1.9k for Claude Code bare mode — harness overhead is
measurable and differs.
