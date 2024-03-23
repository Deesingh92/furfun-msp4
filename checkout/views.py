# views.py

from django.shortcuts import render

def checkout(request):
    # Assuming you have a cart stored in the session
    cart = request.session.get('cart', [])
    
    # Calculate total cost of items in the cart
    cart_total = sum(item['price'] * item['quantity'] for item in cart)
    
    # Check if the request is POST and process the form data if so
    if request.method == 'POST':
        # Retrieve form data
        fullname = request.POST.get('fullname')
        # Process billing information
        
        # Redirect to a thank you page or order confirmation page
        return redirect('order_confirmation')  # Adjust URL name as needed

    # Render the checkout.html template with cart data
    return render(request, 'checkout/checkout.html', {'cart': cart, 'cart_total': cart_total})
