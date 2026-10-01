# Demo backup pack

If a live beat fails on stage, present from these records instead — they are
the actual outputs of the eval runs from 2026-09-30, not mock-ups.

> **Environment warning:** All proof in this pack ran in Helm's environment
> (root VM, Claude Code 2.1.285, apiKeyHelper auth), NOT on Samuel's
> presentation machine. A live divergence (versions, permissions, trust
> state) is not a contradiction — the pack records what happened in Helm's
> environment; the presentation machine was never tested.

| Beat | Backup file | What it proves |
|------|-------------|----------------|
| Cross-tool continuity (E2) | `e2-continuity-claude-answers.md` | Claude answered 5/5 probes from a Copilot session record (scope: Copilot→Claude only, n=1, read-only probes; reverse direction untested) |
| Continuity baseline | `e2-baseline-no-wiki.md` | Same probes, wiki removed: 5/5 "not recorded", nothing invented |
| Failure capture (E4) | `e4-events.md` + `e4-claude-transcript-summary.md` | 5/5 induced failures landed as JSONL events (Claude) |
| Same key, both harnesses | `byok-proof.md` | Copilot ran on the Anthropic key; zero GitHub AI Credits metered |
| Skill parity (E1) | `evals/results/2026-09-30-E1-claude.md` | Both tools invoked `session-harden` by name in fresh installs (Claude leg: the session-file write was permission-blocked; discovery inferred from invocation) |
| Agent write task — pilot fabrication (E6) | `E6-pilot-copilot-fabrication.txt` | Fabrication exhibit (S6b pilot): Copilot reported "22 passed" and wrote zero files (`Changes +0 -0`) — failure caught by disk grading. Superseded by the pre-approved rerun: PROVEN n=1, 20/20 independently re-run (see `E6-pilot-notes.md`) |
| Agent write task — pilot notes + reruns (E6) | `E6-pilot-notes.md` | Pilot record (S6a blocked on write approval; S6b pilot fabrication) with rerun verdicts: S6a PROVEN (Claude pre-approved rerun, 13/13 independently re-run) and S6b pre-approved rerun PROVEN n=1 (20/20 independently re-run). The pilot framing is superseded by the reruns recorded at the top of the file |

Rule: if the live run contradicts a backup, the live run wins and the backup
gets corrected after — never the other way around.
