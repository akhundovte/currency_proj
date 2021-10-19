import decimal


def decimal_format(value, decimal_places):
    """format_number() - django.db.backends.utils.py"""
    context = decimal.getcontext().copy()
    return value.quantize(decimal.Decimal(1).scaleb(-decimal_places), context=context)
