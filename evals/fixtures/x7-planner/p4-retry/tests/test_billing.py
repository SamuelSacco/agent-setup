from app.billing import charge

def test_charge_idempotent():
    p1 = charge("p1", 500, "tok", "key-1")
    p2 = charge("p1", 500, "tok", "key-1")
    assert p1 is p2
