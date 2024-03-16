from django.shortcuts import render
from .models import Product

# Create your views here.

def shop(request):
    """ A view to show all products """

    products = Product.objects.all()

    context = {
        'products': products,
    }

    return render(request, 'shop/shop.html', context)