from invoice import refund

def test_unopened_full():
    assert refund(10000, opened=False, defective=False) == 10000

def test_opened_restocking_fee_12pct():
    assert refund(10000, opened=True, defective=False) == 8800

def test_defective_opened_fee_waived():
    assert refund(10000, opened=True, defective=True) == 10000

def test_defective_unopened_full():
    assert refund(10000, opened=False, defective=True) == 10000

def test_fee_half_up_int_cents():
    r = refund(999, opened=True, defective=False)
    assert r == 879 and type(r) is int
