from django import template
from django.db.models import F

from core.models import Item

register = template.Library()


@register.simple_tag
def get_low_stock_items():
    return Item.objects.filter(stock__lte=F('stock_threshold'))