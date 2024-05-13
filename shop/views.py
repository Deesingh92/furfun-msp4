from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from .models import Product, Category
from django.db.models.functions import Lower
from django.contrib.auth.decorators import login_required
from .forms import ProductForm



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

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('shop')
    else:
        form = ProductForm()
    return render(request, 'shop/add_product.html', {'form': form})


@login_required
def edit_product(request, product_id):
    """A view to edit an existing product"""
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            print("Form is valid.")
            form.save()
            print("Product updated successfully.")
            return redirect('product_detail', product_id=product_id)  # Redirect to the product detail page
        else:
            print("Form errors:", form.errors)
    else:
        form = ProductForm(instance=product)
    return render(request, 'shop/edit_product.html', {'form': form, 'product': product})


@login_required
def delete_product(request, product_id):
    """A view to delete an existing product"""
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('shop')
    return render(request, 'shop/delete_product.html', {'product': product})
