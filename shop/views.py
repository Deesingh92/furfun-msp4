from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.db.models.functions import Lower

def shop(request):
    """ A view to show all products """

    products = Product.objects.all()
    all_categories = Category.objects.all()
    categories = all_categories  # Initialize categories with all categories by default

    query = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'name_lower'
                products = products.annotate(name_lower=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)
            
        if 'category' in request.GET:
            selected_categories = request.GET.getlist('category')
            products = products.filter(category__name__in=selected_categories)
            # Update categories to only include selected categories
            categories = all_categories.filter(name__in=selected_categories)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'includes/header.html', context)

def product_detail(request, product_id):
    """A view to display details of a specific product"""

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product
    }

    return render(request, 'shop/product_detail.html', context)
