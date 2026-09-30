# Live Demo Script

Runtime target: 8–10 minutes inside the presentation. Every step has a 
fallback — if a live call stalls, show the recorded artifact and say so. 
Never fake a live result.

## Setup (before the talk)
- [ ] Both CLIs authenticated (`claude auth status`, one `copilot` smoke prompt)
- [ ] Fresh clone of this repo; `./scripts/install.sh` NOT yet run (we run it live)
- [ ] Terminal in iTerm2, large font, repo root
- [ ] Backup: screenshots/recordings of each step in `docs/demo-backup/`

## Act 1 — One install, both tools (E1)
1. Show `canonical/skills/session-harden.md` — one file, provider-neutral.
2. Run `./scripts/install.sh`. Show the tree: `.claude/skills/...` and 
   `.github/skills/...` written from the same source.
3. Launch `claude`, ask it to list skills → `session-harden` present. Quit.
4. Launch `copilot`, same ask → same skill. 
5. Say the honest line: "File placement is proven; discovery is what you just 
   saw. This is eval E1, and it just flipped to PROVEN."

## Act 2 — Cross-tool continuity (E2)
1. In Claude: "Add a health-check endpoint to the demo service, log the 
   session, harden the wiki." Let it work briefly.
2. Show `wiki/sessions/<today>-claude-*.md` and the new note it created.
3. Quit Claude. Launch Copilot cold.
4. Ask: "What did the last session change, why, and what failed?"
5. Copilot answers from the shared session log. 
6. Honest line: "No copy-paste. The wiki is the shared memory. Eval E2."

## Act 3 — The failure that became data (E4)
1. Ask either tool to run the demo's intentionally broken command 
   (`python` on a python3-only path).
2. Show `wiki/telemetry/events.jsonl` — a structured failure event, captured 
   by the hook, never stuffed into the prompt.
3. `scripts/sidecar.sh summary` — counts by kind. "Telemetry lives outside 
   the context window; only summaries come back in."

## Act 4 — The critic (tips, live if time)
1. Copilot: "Rubber duck your plan" on a small change — show the cross-model 
   critique (Claude session → GPT critic or vice versa).
2. Optional Claude: `/advisor` on a design question — show the consult.
3. Frame: "Both vendors now pair a driver with a second model's judgment. 
   Different philosophies: stronger same-vendor advisor vs cross-vendor critic."

## Fallbacks
- Auth/network failure → `docs/demo-backup/` recordings, narrate the same script.
- A tool doesn't discover the skill → that's a REFUTED E1 on stage; say what 
  the adapter fix is (format/path) and show the canonical file. Honesty is 
  the brand of this talk.
