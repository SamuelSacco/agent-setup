from dataclasses import dataclass

@dataclass
class Product:
    sku: str
    name: str
    price_cents: int

@dataclass
class StockLevel:
    sku: str
    on_hand: int
    reorder_point: int  # alert/reorder threshold for this sku
