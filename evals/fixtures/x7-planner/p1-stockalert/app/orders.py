from app.alerts import notify_order_shipped
from app.inventory import adjust_stock

def create_order(order_id: str, sku: str, qty: int, buyer_email: str) -> None:
    adjust_stock(sku, -qty)

def ship_order(order_id: str, buyer_email: str) -> None:
    notify_order_shipped(order_id, buyer_email)
