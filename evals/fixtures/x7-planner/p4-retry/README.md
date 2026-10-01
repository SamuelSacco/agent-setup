# Payloop
Payment service. Layout: `app/billing.py` charging,
`app/worker.py` background queue worker, `app/api.py` HTTP layer,
`app/ledger.py` accounting entries, `app/refunds.py` refunds.
Tests in `tests/`. Run: `python -m pytest tests/ -q`.
