---
id: billing
title: Billing rules for invoice totals
type: reference
status: active
created: 2026-02-10
updated: 2026-03-02
verified: 2026-03-02
relates_to: [money-convention]
sources: []
tags: [billing]
---

# Billing rules

- Tax is charged on the **full pre-discount subtotal**.
- A discount is a loyalty credit: it is subtracted **after** tax is
  added, never before. A discount does not reduce the taxable amount.
- Shipping is **tax-exempt**: shipping is added at the end and is
  never part of the taxable amount.
- Tax amounts are rounded half-up to the nearest cent (see
  [[money-convention]]).

So: total = subtotal + tax(subtotal) + shipping - discount.
