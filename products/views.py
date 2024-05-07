from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from profiles.models import Wishlist, UserProfile
from .models import Product, Category
from .forms import SortForm

def all_products(request):
    query = request.GET.get('q')
    sort_by = request.GET.get('sort_by', 'name')  # Default is 'name'
    if sort_by == 'recent':
        sort_by = '-date_added' 
    elif sort_by == 'highest_rating':
        sort_by = '-rating'  
    if query:
        products = Product.objects.filter(name__icontains=query).order_by(sort_by)
    else:
        products = Product.objects.all().order_by(sort_by)
        if 'q' in request.GET:  # Check if 'q' parameter is in the request
            messages.error(request, 'Please enter a search term.')  # Error message
    form = SortForm(request.GET)
    return render(request, 'products/products.html', {'products': products, 'form': form})


def products_by_category(request, category_slug):
    sort_by = request.GET.get('sort_by', 'name')  # Default is 'name'
    category = get_object_or_404(Category, slug=category_slug)
    subcategories = Category.objects.filter(parent=category)
    products = Product.objects.filter(Q(category=category) | Q(category__in=subcategories)).order_by(sort_by)
    form = SortForm(request.GET)
    return render(request, 'products/products.html', {'products': products, 'category_name': category.name, 'category': category, 'form': form})


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    context = {
        'product': product,
    }
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        wishlist, created = Wishlist.objects.get_or_create(user=user_profile)
        context['wishlist'] = wishlist
    return render(request, 'products/product_detail.html', context)