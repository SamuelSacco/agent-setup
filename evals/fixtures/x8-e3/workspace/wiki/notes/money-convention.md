---
id: money-convention
title: Money convention
type: procedure
status: active
created: 2026-02-10
updated: 2026-03-02
verified: 2026-03-02
relates_to: [billing]
sources: []
tags: [money, convention]
---

# Money convention

- Every money function takes **integer cents** and returns
  **integer cents**. Returning float dollars is a convention
  violation, even if the numeric value looks right.
- Rounding is **half-up**, always. Python's built-in `round()`
  (banker's rounding) must not be used for money.
- Tax is included in a quote's returned total.
