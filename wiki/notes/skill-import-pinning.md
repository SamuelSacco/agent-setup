---
id: skill-import-pinning
title: Claim — hash-pin + audit-check enforcement on skill import (prototype)
type: claim
status: active
created: 2026-09-30
updated: 2026-09-30
verified: 2026-09-30
relates_to: [install-surfaces]
sources: []
tags: [skills, supply-chain, security]
verdict: PROVEN (prototype scope)
evidence: evals/results/2026-09-30-X6-hashpin-prototype.md
---

Ledger S19. Built 2026-09-30 (backlog X6) against packet finding 5
("nobody enforces snapshot + hash-pin + audit-check on import"):
`scripts/import_skill.py` audits a candidate skill, refuses on
critical findings (instruction-override phrasing, pipe-to-shell,
credential-store reference combined with a transmit verb), flags
warnings (URLs, shell fences, strong imperatives), imports into
`canonical/skills/`, and records a SHA-256 pin in
`canonical/skill-pins.json`; `verify` re-hashes every pinned skill.

Preregistered demo passed: clean skill imported and pinned (pin equals
an independent `sha256sum`); planted tampered skill REFUSED (4 critical
findings, no file, no pin); post-import edit caught by `verify`
(MISMATCH) and restored by `--force` re-import.

Prototype limits: pattern-list audit (named classes only), no
signatures or publisher identity, not wired into `install.sh`. This
closes the UNBUILT status; it is not production enforcement.
