from django.shortcuts import render, get_object_or_404
from .models import Product
from .forms import SortForm

def all_products(request):
    query = request.GET.get('q')
    sort_by = request.GET.get('sort_by', 'name')  # Default is 'name'
    if query:
        products = Product.objects.filter(name__icontains=query).order_by(sort_by)
    else:
        products = Product.objects.all().order_by(sort_by)
    form = SortForm(request.GET)
    return render(request, 'products/products.html', {'products': products, 'form': form})

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }
    return render(request, 'products/product_detail.html', context)