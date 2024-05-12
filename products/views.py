from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from profiles.models import Wishlist, UserProfile
from .models import Product, Category
from .forms import SortForm, ProductForm

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
        if request.user.is_superuser:
            form = ProductForm(instance=product)
            context['form'] = form
    return render(request, 'products/product_detail.html', context)


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'The advert has been added to your site.')
            return redirect('home')
    else:
        form = ProductForm()
    return render(request, 'products/add_product.html', {'form': form})

def edit_product(request, product_id):
    if not request.user.is_superuser:
        messages.error(request, 'Only superusers can edit products.')
        return redirect('home')

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            print(form.cleaned_data)  # print form data
            product = form.save()
            messages.success(request, f'Successfully updated product {product.name}!')
            return redirect('product_detail', product_id=product.id)
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/edit_product.html', {'form': form})

def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect('home')