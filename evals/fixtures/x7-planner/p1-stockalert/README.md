# Stockroom
Small inventory service. Layout: `app/models.py` data classes,
`app/inventory.py` stock operations, `app/orders.py` order flow,
`app/alerts.py` outbound email alerts, `app/reports.py` reporting,
`app/scheduler.py` periodic jobs, `app/config.py` settings.
Tests in `tests/`. Run: `python -m pytest tests/ -q`.
