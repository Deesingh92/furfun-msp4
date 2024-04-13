from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from .models import Order, OrderLineItem
from cart.models import Product  # Import Product model
from cart.contexts import cart_contents
from django.views.decorators.http import require_POST
from django.http import HttpResponse

@require_POST
def cache_checkout_data(request):
    try:
        # Your code for caching checkout data
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)

def checkout(request):
    cart = request.session.get('cart', {})
    print("Cart Contents:", cart)  # Debug print statement
    if not cart:
        messages.error(request, "There's nothing in your cart at the moment")
        print("Redirecting to shop because cart is empty")  # Debug print statement
        return redirect(reverse('shop'))

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.save()

            for product_id, quantity in cart.items():
                product = Product.objects.get(id=product_id)
                order_line_item = OrderLineItem(
                    order=order,
                    product=product,
                    quantity=quantity,
                )
                order_line_item.save()

            request.session['save_info'] = 'save-info' in request.POST
            del request.session['cart']  # Clear cart after checkout
            return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(request, 'There was an error with your form. Please double check your information.')
    else:
        form = OrderForm()

    template = 'checkout/checkout.html'
    context = {
        'form': form,
        'cart': cart_contents(request),
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'client_secret': 'test client secret',  
    }

    return render(request, template, context)

def checkout_success(request, order_number):
    order = Order.objects.get(order_number=order_number)
    messages.success(request, f'Order successfully processed! Your order number is {order_number}. '
                              f'A confirmation email will be sent to {order.email}.')

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
