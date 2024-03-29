from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product
from cart.models import Cart


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    cart.add(product=product)
    messages.success(request, f"{product.name} added to your cart.")
    return redirect('cart_detail') 

def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    cart.remove(product)
    messages.success(request, f"{product.name} removed from your cart.")
    return redirect('cart_detail')  

def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    messages.success(request, "Your cart is cleared.")
    return redirect('cart_detail') 

def cart_detail(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        cart = None
    return render(request, 'cart/cart.html', {'cart': cart})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'shop/product_detail.html', {'product': product})