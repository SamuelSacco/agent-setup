#!/usr/bin/env python3
"""Seed a synthetic wiki for eval E5 (context cost). 40 notes: 25 active,
15 stale/archived. Deterministic; writes evals/fixtures/wiki-seed/."""
import random, shutil
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "evals" / "fixtures" / "wiki-seed"
random.seed(42)
TOPICS = ["auth","caching","queues","logging","retries","schema","testing","deploys",
          "metrics","search","uploads","billing","sessions","errors","config",
          "indexing","webhooks","limits","audits","backups","flags","routing",
          "timeouts","secrets","migrations","queues-2","search-2","auth-2","api","cli"]
BODY = ("This note records how the {t} subsystem behaves, why it was built this way, "
        "and what to check before changing it. " * 6)

if OUT.exists(): shutil.rmtree(OUT)
(OUT).mkdir(parents=True)
for i, t in enumerate(TOPICS[:25]):
    (OUT / f"{t}.md").write_text(f"""---
id: {t}
title: {t.title()} notes
type: reference
status: active
created: 2026-09-01
updated: 2026-09-20
verified: 2026-09-20
relates_to: [seed-index]
sources: []
tags: [seed]
---

{BODY.format(t=t)}
""")
for i, t in enumerate(["old-api","legacy-auth","v1-queue","deprecated-cache","old-flags"] + [f"stale-{j}" for j in range(10)]):
    (OUT / f"{t}.md").write_text(f"""---
id: {t}
title: {t} (retired)
type: reference
status: archived
created: 2026-01-15
updated: 2026-03-01
verified: 2026-03-01
relates_to: [seed-index]
sources: []
tags: [seed]
---

{BODY.format(t=t)}
""")
print(f"seeded {len(list(OUT.glob('*.md')))} notes in {OUT}")
