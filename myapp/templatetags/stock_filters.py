from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def subtract(value, arg):
    try:
        return Decimal(value) - Decimal(arg)
    except (ValueError, TypeError):
        return value

@register.filter
def divide(value, arg):
    try:
        return Decimal(value) / Decimal(arg)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0

@register.filter
def multiply(value, arg):
    try:
        return Decimal(value) * Decimal(arg)
    except (ValueError, TypeError):
        return value 