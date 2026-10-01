---
id: receipts-decision
title: Decision — how receipts are stored
type: decision
status: active
created: 2026-02-18
updated: 2026-02-18
verified: 2026-02-18
relates_to: [import-history]
sources: []
tags: [decision, storage]
---

# Decision: receipts storage

- Decided 2026-02-18: receipts are stored as an **append-only
  JSONL file** (one JSON object per line).
- SQLite was considered and rejected: there is a **single writer**
  and every consumer reads files directly, so a database earns
  nothing yet.
- Revisit this decision when any of these happens: a **second
  concurrent writer** appears, the receipts file exceeds
  **50,000 lines**, or **cross-machine queries** are needed.
