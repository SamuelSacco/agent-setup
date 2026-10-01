from app.alerts import send_email
from app.config import ALERT_EMAIL
from app.inventory import all_levels

def weekly_stock_report() -> None:
    lines = [f"{l.sku}: {l.on_hand}" for l in all_levels()]
    send_email(ALERT_EMAIL, "Weekly stock report", "\n".join(lines))
