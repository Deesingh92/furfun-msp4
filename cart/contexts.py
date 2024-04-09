from django.shortcuts import get_object_or_404
from .models import Order, CartItem
from shop.models import Product

def cart_contents(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    product_count = 0

    for item_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=item_id)
        total += quantity * product.price
        product_count += quantity
        cart_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'product': product,
        })

    # Fetch cart items related to the current user, if using authentication
    if request.user.is_authenticated:
        user_cart_items = CartItem.objects.filter(cart__user=request.user)
        for item in user_cart_items:
            cart_items.append({
                'item_id': item.product.id,
                'quantity': item.quantity,
                'product': item.product,
            })

    return {
        'cart_items': cart_items,
        'total': total,
        'product_count': product_count,
    }
