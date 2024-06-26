from .models import Cart

def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        return cart
    else:
        if 'cart' not in request.session:
            # Initialize an empty cart dictionary in the session
            request.session['cart'] = {}
        return request.session.get('cart', {})  # Ensure that we return a dictionary
