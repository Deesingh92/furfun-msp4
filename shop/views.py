from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.db.models.functions import Lower

def shop(request):
    """ A view to show all products """

    products = Product.objects.all()
    all_categories = Category.objects.all()
    categories = all_categories 

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
            elif sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        if 'category' in request.GET:
            selected_categories = request.GET.getlist('category')
            if selected_categories:
                products = products.filter(category__name__in=selected_categories)
                categories = all_categories.filter(name__in=selected_categories)
            else:
                categories = None

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


def add_product(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        Product.objects.create(name=product_name)
        return redirect('product_list')
    else:
        return render(request, 'shop/add_product.html')