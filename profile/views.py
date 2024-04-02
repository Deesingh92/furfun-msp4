from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Order

@login_required
def profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    context = {
        'user_profile': user_profile
    }
    return render(request, 'profile.html', context)

def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'order_history.html', {'orders': orders})

def order_detail(request, order_number):
    order = Order.objects.get(order_number=order_number)
    return render(request, 'order_detail.html', {'order': order})

