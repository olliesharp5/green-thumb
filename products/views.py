from django.shortcuts import render
from .models import Product

def all_products(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()
    return render(request, 'products/products.html', {'products': products})