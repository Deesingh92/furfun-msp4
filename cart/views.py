from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product
from cart.models import Cart

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'shop/product_detail.html', {'product': product})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    cart.add(product=product)
    messages.success(request, f"{product.name} added to your cart.")
    return redirect('cart/cart.html')

def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    cart.remove(product)
    messages.success(request, f"{product.name} removed from your cart.")
    return redirect('cart/cart.html')

def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    messages.success(request, "Your cart is cleared.")
    return redirect('cart/cart.html')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart.html', {'cart': cart})
