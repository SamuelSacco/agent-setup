from invoice import quote

def test_returns_int_cents():
    r = quote(1000, 1, 0)
    assert r == 1000 and type(r) is int

def test_half_up_not_bankers():
    r = quote(105, 1, 1000)
    assert r == 116 and type(r) is int

def test_qty_and_tax():
    assert quote(999, 3, 825) == 3244

def test_no_tax_int():
    assert quote(250, 4, 0) == 1000
