from app.config import ALERT_EMAIL

_sent: list[dict] = []

def send_email(to: str, subject: str, body: str) -> None:
    """Single outbound-email path for the whole app."""
    _sent.append({"to": to, "subject": subject, "body": body})

def notify_order_shipped(order_id: str, buyer_email: str) -> None:
    send_email(buyer_email, f"Order {order_id} shipped", "Your order is on its way.")
