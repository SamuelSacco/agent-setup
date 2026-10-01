from invoice import invoice_total

def test_discount_after_tax_shipping_present():
    assert invoice_total(10000, 1000, 500, 1000) == 10500

def test_tax_on_full_subtotal_no_discount():
    assert invoice_total(20000, 0, 999, 825) == 22649

def test_full_discount_still_taxed_on_subtotal():
    assert invoice_total(5000, 5000, 0, 1000) == 500

def test_tax_half_up_and_shipping_exempt():
    assert invoice_total(1050, 100, 200, 500) == 1203

def test_half_up_tax_no_discount():
    assert invoice_total(1050, 0, 0, 500) == 1103
