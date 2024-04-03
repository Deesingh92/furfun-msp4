from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product, CartItem, Cart
from django.contrib.auth.decorators import login_required

def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart.html', {'cart': cart})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f'Updated {product.name} quantity to {cart_item.quantity}')
    else:
        messages.success(request, f'Added {product.name} to your cart')

    return redirect('cart')


@login_required
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    cart.remove(product)
    messages.success(request, f"{product.name} removed from your cart.")
    return redirect('cart_detail')  

@login_required
def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    messages.success(request, "Your cart is cleared.")
    return redirect('cart_detail') 

@login_required
def cart_detail(request):
    cart_items = CartItem.objects.filter(cart__user=request.user)
    cart_total = sum(item.get_item_total() for item in cart_items)
    return render(request, 'cart/cart.html', {'cart_items': cart_items, 'cart_total': cart_total})
