# Demo backup pack

If a live beat fails on stage, present from these records instead — they are
the actual outputs of the eval runs from 2026-09-30, not mock-ups.

| Beat | Backup file | What it proves |
|------|-------------|----------------|
| Cross-tool continuity (E2) | `e2-continuity-claude-answers.md` | Claude answered 5/5 probes from a Copilot session record |
| Continuity baseline | `e2-baseline-no-wiki.md` | Same probes, wiki removed: 5/5 "not recorded", nothing invented |
| Failure capture (E4) | `e4-events.md` + `e4-claude-transcript-summary.md` | 5/5 induced failures landed as JSONL events (Claude) |
| Same key, both harnesses | `byok-proof.md` | Copilot ran on the Anthropic key; zero GitHub AI Credits metered |
| Skill parity (E1) | `evals/results/2026-09-30-E1-claude.md` | Both tools invoked `session-harden` by name in fresh installs |

Rule: if the live run contradicts a backup, the live run wins and the backup
gets corrected after — never the other way around.
