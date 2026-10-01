---
id: import-history
title: History of the invoice importer
type: reference
status: active
created: 2026-03-10
updated: 2026-03-10
verified: 2026-03-10
relates_to: [receipts-decision]
sources: []
tags: [history, importer]
---

# Importer history

- February 2026: the first CSV import attempt failed. It produced
  **347 duplicate invoices** because the importer keyed rows on row
  number instead of the vendor's `external_id` field. The fix was
  to dedupe on `external_id`.
- March 2026: the project chose the **CSV bulk importer** over the
  vendor API importer. Reason: the vendor API is capped at
  **100 requests per day** and offers **no bulk endpoint**, so
  importing a month of invoices over the API would take weeks.
  The API importer was the alternative considered and rejected.
