from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Order, CartItem, Cart
from shop.models import Product
from .utils import get_or_create_cart

def cart_contents(request):
    cart = request.session.get('cart', {})
    cart_items = []
    
    if isinstance(cart, dict) and 'cart_id' in cart:
        cart_id = cart['cart_id']
        try:
            cart_model = Cart.objects.get(pk=cart_id)
            cart_items = cart_model.cart_items.all()
        except Cart.DoesNotExist:
            pass
    elif isinstance(cart, dict) and 'user_id' in cart:  
        user_id = cart['user_id']
        try:
            user = User.objects.get(pk=user_id)
            cart_model = user.cart
            cart_items = cart_model.cart_items.all()
        except User.DoesNotExist:
            pass
    
    return {'cart_items': cart_items}
