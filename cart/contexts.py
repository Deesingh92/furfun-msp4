from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Order, CartItem
from shop.models import Product
from .utils import get_or_create_cart

@login_required
def cart_contents(request):
    cart = get_or_create_cart(request)
    cart_items = cart.cart_items.all()
    cart_total = sum(item.get_item_total() for item in cart_items)
    return {
        'cart_items': cart_items,
        'cart_total': cart_total,
    }
