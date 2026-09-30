---
id: telemetry-storage
title: Telemetry storage — JSONL/SQLite before Postgres
type: decision
status: active
created: 2026-09-30
updated: 2026-09-30
verified: 2026-09-30
relates_to: [session-lifecycle]
sources: []
tags: [telemetry, storage]
---

Telemetry (hook events, failures, token counts) is stored as append-only JSONL 
at `wiki/telemetry/events.jsonl`, queried with jq or loaded into SQLite when 
needed. Postgres is **not** used.

Why: single writer per workspace, low volume, file-native consumers (agents read 
files). Postgres earns its place only with concurrent writers, cross-machine 
queries, or search/retention beyond flat files — none of which a single-dev 
workspace has. Revisit if the setup goes multi-user or org-wide.
