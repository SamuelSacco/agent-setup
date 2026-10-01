from app.models import StockLevel

_levels: dict[str, StockLevel] = {}

def set_level(level: StockLevel) -> None:
    _levels[level.sku] = level

def get_stock_level(sku: str) -> StockLevel | None:
    return _levels.get(sku)

def adjust_stock(sku: str, delta: int) -> StockLevel:
    level = _levels[sku]
    level.on_hand += delta
    return level

def all_levels() -> list[StockLevel]:
    return list(_levels.values())
