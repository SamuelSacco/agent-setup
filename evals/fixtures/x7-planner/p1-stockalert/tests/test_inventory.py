from app.inventory import adjust_stock, set_level
from app.models import StockLevel

def test_adjust_stock():
    set_level(StockLevel("A1", 5, 2))
    assert adjust_stock("A1", -1).on_hand == 4
