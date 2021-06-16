from django import template
from catalogue.models import Order
from django.contrib.auth.models import User

register = template.Library()

@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False)
        if qs.exists():
            order = qs[0]
            return order.items.count()
        return 0


@register.filter()
def add(value, arg):
    return value + arg
