---
id: refunds
title: Refund policy
type: procedure
status: active
created: 2026-02-12
updated: 2026-03-05
verified: 2026-03-05
relates_to: [billing, money-convention]
sources: []
tags: [refunds]
---

# Refund policy

- Unopened items: full refund of the amount paid.
- Opened items: a **12% restocking fee** is deducted. The fee is
  rounded half-up to the nearest cent; refund = amount - fee.
- Defective items: **always a full refund** — the restocking fee
  is waived even if the item was opened.
- Signature: `refund(amount_cents, *, opened, defective)` returning
  integer cents.
