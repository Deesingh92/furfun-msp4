from django.shortcuts import get_object_or_404
from .models import Order, CartItem
from shop.models import Product
from .utils import get_or_create_cart


def cart_contents(request):
    try:
        cart = get_or_create_cart(request)
        cart_items = cart.cart_items.all()
        cart_total = sum(item.get_item_total() for item in cart_items)
    except Exception as e:
        cart_items = []
        cart_total = 0
    
    return {
        'cart_items': cart_items,
        'cart_total': cart_total,
    }
