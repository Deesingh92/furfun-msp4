from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib import messages
from .models import Product, CartItem, Cart
from .utils import get_or_create_cart
from django.contrib.auth.decorators import login_required
from decimal import Decimal

def view_cart(request):
    cart = get_or_create_cart(request)
    return render(request, 'cart.html', {'cart': cart})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart = get_or_create_cart(request)

    # Check if quantity is specified in the request
    quantity = int(request.POST.get('quantity', 1))

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        # Increment quantity by the specified amount
        cart_item.quantity += quantity
        cart_item.save()
        messages.success(request, f'Updated {product.name} quantity to {cart_item.quantity}')
    else:
        # Set quantity to the specified amount
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, f'Added {quantity} {product.name}(s) to your cart')

    # Update session cart
    request.session['cart'] = cart.id

    print("Cart Contents:", cart.cart_items.all())  # Print updated cart items
    return redirect('cart')

@login_required
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(cart__user=request.user, product=product)
    cart_item.delete()
    messages.success(request, f"{product.name} removed from your cart.")
    
    # Update session cart
    request.session['cart'] = cart_item.cart.id

    print("Cart Contents:", CartItem.objects.filter(cart__user=request.user))  # Print remaining cart items
    return redirect('cart_detail')  

@login_required
def clear_cart(request):
    cart = Cart.objects.get(user=request.user)
    cart.cart_items.all().delete()
    messages.success(request, "Your cart is cleared.")
    
    # Update session cart
    request.session.pop('cart', None)

    return redirect('cart_detail') 

@login_required
def cart_detail(request):
    cart_id = request.session.get('cart')
    if cart_id:
        cart = Cart.objects.get(id=cart_id)
        cart_items = cart.cart_items.all()

        
        return render(request, 'cart/cart.html', {'cart_items': cart_items})
    else:
        return redirect('shop')