from dataclasses import dataclass

@dataclass
class Payment:
    payment_id: str
    amount_cents: int
    status: str = "pending"  # pending -> succeeded | failed
    idempotency_key: str = ""

_by_key: dict[str, Payment] = {}

def charge(payment_id: str, amount_cents: int, card_token: str,
           idempotency_key: str) -> Payment:
    """Charge a card. Idempotent: a repeat call with the same
    idempotency_key returns the original Payment and does NOT
    charge again. Callers retrying a charge must reuse the key."""
    if idempotency_key in _by_key:
        return _by_key[idempotency_key]
    payment = Payment(payment_id, amount_cents, "succeeded", idempotency_key)
    _by_key[idempotency_key] = payment
    return payment

def get_payment(payment_id: str) -> Payment | None:
    for p in _by_key.values():
        if p.payment_id == payment_id:
            return p
    return None
