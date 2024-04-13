from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product, CartItem, Cart
from django.contrib.auth.decorators import login_required
from .utils import get_or_create_cart

def view_cart(request):
    print("User:", request.user)
    cart = get_or_create_cart(request)
    print("Cart ID:", cart.id)  # Print the ID of the cart
    return render(request, 'cart.html', {'cart': cart})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart = get_or_create_cart(request)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f'Updated {product.name} quantity to {cart_item.quantity}')
    else:
        messages.success(request, f'Added {product.name} to your cart')
    
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

    print("Cart Contents:", cart.cart_items.all())  # Print cleared cart items
    return redirect('cart_detail') 

@login_required
def cart_detail(request):
    cart_id = request.session.get('cart')
    if cart_id:
        cart = Cart.objects.get(id=cart_id)
        cart_items = cart.cart_items.all()
        cart_total = sum(item.get_item_total() for item in cart_items)
        print("Cart Contents:", cart_items)  # Print cart items
        print("Cart Total:", cart_total)  # Print cart total
        return render(request, 'cart/cart.html', {'cart_items': cart_items, 'cart_total': cart_total})
    else:
        # Handle case where cart is empty or not found in session
        print("Session Cart ID not found or cart is empty")
        return redirect('shop')
