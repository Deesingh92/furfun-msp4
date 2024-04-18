from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings
from .forms import OrderForm
from .models import Order, OrderLineItem
from cart.models import Product 
from cart.contexts import cart_contents
from django.views.decorators.http import require_POST
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

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
    if not cart:
        messages.error(request, "There's nothing in your cart at the moment")
        return redirect(reverse('shop'))

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            try:
                order = form.save(commit=False)
                order.save()

                order_items = []
                total_amount = 0

                for product_id, quantity in cart.items():
                    try:
                        product = Product.objects.get(id=product_id)
                        total_amount += product.price * quantity
                        order_items.append(OrderLineItem(order=order, product=product, quantity=quantity))
                    except Product.DoesNotExist:
                        messages.warning(request, f'Product with ID {product_id} does not exist.')

                OrderLineItem.objects.bulk_create(order_items)

                session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[
                        {
                            'price_data': {
                                'currency': 'gbp',
                                'product_data': {
                                    'name': 'Your Product Name',
                                },
                                'unit_amount': int(total_amount * 100),  # Stripe expects amount in cents
                            },
                            'quantity': 1,
                        },
                    ],
                    mode='payment',
                    success_url=request.build_absolute_uri(reverse('checkout_success', args=[order.order_number])),
                    cancel_url=request.build_absolute_uri(reverse('checkout')),
                )

                return redirect(session.url)
            except Exception as e:
                messages.error(request, 'There was an error processing your order. Please try again later.')
        else:
            messages.error(request, 'There was an error with your form. Please double check your information.')
    else:
        form = OrderForm()

    latest_order = Order.objects.last()

    template = 'checkout/checkout.html'
    context = {
        'order_form': form,
        'cart': cart_contents(request),
        'latest_order': latest_order,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    }

    return render(request, template, context)

def checkout_success(request, order_number):
    try:
        order = Order.objects.get(order_number=order_number)
        messages.success(request, f'Order successfully processed! Your order number is {order_number}. '
                                  f'A confirmation email will be sent to {order.email}.')
        template = 'checkout/checkout_success.html'
        context = {
            'order': order,
        }
        return render(request, template, context)
    except Order.DoesNotExist:
        messages.error(request, f'Order with number {order_number} does not exist.')
        return redirect(reverse('shop'))
