from invoice import invoice_total, quote

def test_total_no_discount_no_shipping():
    assert invoice_total(10000, 0, 0, 1000) == 11000

def test_quote_simple():
    # legacy float-dollars behaviour, simple case
    assert quote(1000, 1, 0) == 10.0
