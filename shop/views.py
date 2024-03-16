from django.shortcuts import render
from .models import Product, Category
from django.db.models.functions import Lower

def shop(request):
    """ A view to show all products """

    products = Product.objects.all()
    categories = Category.objects.all()

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
            categories = request.GET.getlist('category')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

    current_sorting = f'{sort}_{direction}'


    context = {
        'products': products,
        'categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'shop/shop.html', context)




def product_detail(request, product_id):
    """A view to display details of a specific product"""

    product = get_object_or_404(Product, pk=product_id)


    context = {
        'product': product
    }

    return render(request, 'shop/product_detail.html', context)