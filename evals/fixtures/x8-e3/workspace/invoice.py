"""ledgerlite invoice helpers. All amounts are in cents unless a
function says otherwise."""
from decimal import Decimal, ROUND_HALF_UP


def _round_half_up(value):
    return int(Decimal(str(value)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def invoice_total(subtotal_c, discount_c, shipping_c, tax_rate_bp):
    """Total for an invoice. Current implementation — a customer
    reports the total is wrong when a discount and shipping are
    both present. See the bug report in the task."""
    taxable = subtotal_c - discount_c
    tax = _round_half_up(taxable * tax_rate_bp / 10000)
    return taxable + tax + shipping_c


def quote(unit_cents, qty, tax_rate_bp):
    """Price quote. Legacy implementation: works in float dollars
    and uses Python's round()."""
    dollars = unit_cents * qty / 100
    tax = dollars * tax_rate_bp / 10000
    return round(dollars + tax, 2)
