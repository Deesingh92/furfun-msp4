from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product, CartItem, Cart
from django.contrib.auth.decorators import login_required


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    quantity = int(request.POST.get('quantity', 1))  # Retrieve quantity from form
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'price': product.price})
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    messages.success(request, f"{product.name} added to your cart.")
    return redirect('cart_detail')


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

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'shop/product_detail.html', {'product': product})