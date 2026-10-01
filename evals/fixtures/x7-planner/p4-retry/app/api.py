from app.billing import charge

def post_charge(body: dict) -> dict:
    # Synchronous request handler; keep it a single charge() call.
    payment = charge(body["payment_id"], body["amount_cents"],
                     body["card_token"], body["idempotency_key"])
    return {"payment_id": payment.payment_id, "status": payment.status}
