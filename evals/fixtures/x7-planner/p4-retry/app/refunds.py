from app.ledger import record_entry

def refund(payment_id: str, amount_cents: int) -> None:
    record_entry(payment_id, amount_cents, "refund")
