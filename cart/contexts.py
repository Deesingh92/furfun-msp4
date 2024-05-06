from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import CartItem, Product
from .utils import get_or_create_cart


def cart_contents(request):
    try:
        cart = get_or_create_cart(request)
        cart_items = cart.cart_items.all()
        cart_total = sum(item.get_item_total() for item in cart_items)
        product_count = sum(item.quantity for item in cart_items)
    except Exception as e:
        cart_items = []
        cart_total = 0
        product_count = 0
    
    if cart_total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = cart_total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - cart_total
    else:
        delivery = 0
        free_delivery_delta = 0
    
    grand_total = delivery + cart_total
    
    return {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }
