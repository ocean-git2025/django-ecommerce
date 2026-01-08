from django import template
from core.models import Order, ProductFavorite

register = template.Library()


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False)
        if qs.exists():
            return qs[0].items.count()
    return 0


@register.filter
def is_favorited(user, item):
    if user.is_authenticated:
        return ProductFavorite.objects.filter(user=user, item=item).exists()
    return False
