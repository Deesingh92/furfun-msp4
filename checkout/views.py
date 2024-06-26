from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.conf import settings
from .forms import OrderForm
from .models import Order, OrderLineItem
from profiles.models import UserProfile
from profiles.forms import UserProfileForm
from cart.models import Product 
from cart.contexts import cart_contents
from cart.views import clear_cart
from django.views.decorators.http import require_POST
from django.http import HttpResponse
import stripe
import json

@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'cart': json.dumps(request.session.get('cart', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user.username,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, ('Sorry, your payment cannot be '
                                 'processed right now. Please try '
                                 'again later.'))
        return HttpResponse(content=e, status=400)

def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    try:
        # Create PaymentIntent outside the try-except block
        cart = request.session.get('cart', {})
        current_cart = cart_contents(request)
        total = current_cart['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )
    except Exception as e:
        # Handle Stripe errors
        messages.error(request, f"An error occurred while creating PaymentIntent: {str(e)}")
        intent = None

    if request.method == 'POST':
        # Handle form submission
        cart = request.session.get('cart', {})
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }

        order_form = OrderForm(form_data)
        if order_form.is_valid():
            # Process the form data
            pid = request.POST.get('client_secret').split('_secret')[0]
            order = order_form.save(commit=False)
            order.stripe_pid = pid
            order.original_bag = json.dumps(cart)
            order.save()

            # Set the order_number
            order_number = order.order_number

            # Process the cart items and create OrderLineItem instances
            if isinstance(cart, dict):
                for item_id, item_data in cart.items():
                    try:
                        product = Product.objects.get(id=item_id)
                        if isinstance(item_data, int):
                            quantity = item_data
                        else:
                            quantity = item_data['quantity']
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=quantity,
                        )
                        order_line_item.save()
                    except Product.DoesNotExist:
                        # Handle the case when the product doesn't exist
                        messages.error(request, "One of the products in your cart wasn't found in our database. Please call us for assistance!")
                        order.delete()
                        return redirect(reverse('view_cart'))

            # Save the info to the user's profile if all is well
            request.session['save_info'] = 'save-info' in request.POST

            # Clear the cart session
            request.session['cart'] = {}

            return redirect(reverse('checkout_success', args=[order_number]))
        else:
            messages.error(request, 'There was an error with your form. Please double check your information.')
    else:
        # Handle GET request
        if not cart:
            messages.error(request, "There's nothing in your cart at the moment")
            return redirect(reverse('shop'))

        # Attempt to prefill the form with user's profile info
        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                order_form = OrderForm(initial={
                    'full_name': profile.user.get_full_name(),
                    'email': profile.user.email,
                    'phone_number': profile.default_phone_number,
                    'country': profile.default_country,
                    'postcode': profile.default_postcode,
                    'town_or_city': profile.default_town_or_city,
                    'street_address1': profile.default_street_address1,
                    'street_address2': profile.default_street_address2,
                    'county': profile.default_county,
                })
            except UserProfile.DoesNotExist:
                order_form = OrderForm()
        else:
            order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. Did you forget to set it in your environment?')

    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
    }
    if intent:
        context['client_secret'] = intent.client_secret

    return render(request, 'checkout/checkout.html', context)



def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    if order_number:
        order = get_object_or_404(Order, order_number=order_number)

        if request.user.is_authenticated:
            profile = UserProfile.objects.get(user=request.user)
            # Attach the user's profile to the order
            order.user_profile = profile
            order.save()

            # Save the user's info
            if request.session['save_info']:
                profile_data = {
                    'default_phone_number': order.phone_number,
                    'default_country': order.country,
                    'default_postcode': order.postcode,
                    'default_town_or_city': order.town_or_city,
                    'default_street_address1': order.street_address1,
                    'default_street_address2': order.street_address2,
                    'default_county': order.county,
                }
                user_profile_form = UserProfileForm(profile_data, instance=profile)
                if user_profile_form.is_valid():
                    user_profile_form.save()

        messages.success(request, f'Order successfully processed! \
            Your order number is {order_number}. A confirmation \
            email will be sent to {order.email}.')

        # Clear the cart session
        clear_cart(request)

        template = 'checkout/checkout_success.html'
        context = {
            'order': order,
        }

        return render(request, template, context)