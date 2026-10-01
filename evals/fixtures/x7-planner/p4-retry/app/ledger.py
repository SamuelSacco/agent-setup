_entries: list[dict] = []

def record_entry(payment_id: str, amount_cents: int, kind: str) -> None:
    _entries.append({"payment_id": payment_id, "amount_cents": amount_cents, "kind": kind})
