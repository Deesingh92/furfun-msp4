from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product, CartItem, Cart
from django.contrib.auth.decorators import login_required
from .utils import get_or_create_cart

def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
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

    return redirect('cart')

@login_required
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(cart__user=request.user, product=product)
    cart_item.delete()
    messages.success(request, f"{product.name} removed from your cart.")
    return redirect('cart_detail')  

@login_required
def clear_cart(request):
    cart = Cart.objects.get(user=request.user)
    cart.cart_items.all().delete()
    messages.success(request, "Your cart is cleared.")
    return redirect('cart_detail') 

@login_required
def cart_detail(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.cart_items.all()
    cart_total = sum(item.get_item_total() for item in cart_items)
    return render(request, 'cart/cart.html', {'cart_items': cart_items, 'cart_total': cart_total})
