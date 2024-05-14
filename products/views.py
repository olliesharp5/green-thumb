from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.http import require_POST
from profiles.models import Wishlist, UserProfile
from .models import Product, Category, Review
from .forms import SortForm, ProductForm, ReviewForm

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
    reviews = product.reviews.all()
    user_has_reviewed = False
    context = {
        'product': product,
        'reviews': reviews,
    }
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        wishlist, created = Wishlist.objects.get_or_create(user=user_profile)
        context['wishlist'] = wishlist
        if request.user.is_superuser:
            form = ProductForm(instance=product)
            context['form'] = form
        try:
            review = Review.objects.get(product=product, user=request.user)
            review_form = ReviewForm(instance=review)  # pass the review to the form
            user_has_reviewed = True
        except Review.DoesNotExist:
            review_form = ReviewForm()  # if the review does not exist, create an empty form
        context['review_form'] = review_form
    else:
        review_form = ReviewForm()  # if the user is not authenticated, create an empty form
        context['review_form'] = review_form
    context['user_has_reviewed'] = user_has_reviewed
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
            request.session['cart_changed'] = False
            messages.success(request, f'Successfully updated product {product.name}!')
            return redirect('product_detail', product_id=product.id)
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/edit_product.html', {'form': form})

def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        product.delete()
        del cart[str(product_id)]
        request.session['cart'] = cart
        request.session['cart_changed'] = True
        messages.success(request, 'Product deleted and removed from carts!')
    else:
        product.delete()
        request.session['cart_changed'] = False
        messages.success(request, 'Product deleted!')

    return redirect('home')

def create_review(request, product_id):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        print(form)
        if form.is_valid():
            review = form.save(commit=False)
            review.product_id = product_id
            review.user = request.user
            review.save()
            return redirect('product_detail', product_id=product_id)
    else:
        form = ReviewForm()
    return render(request, 'reviews/create_review.html', {'review_form': form})

def update_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    print(form)
    if request.user != review.user:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('product_detail', product_id=review.product.id)
    else:
        form = ReviewForm(instance=review)
    return render(request, 'reviews/update_review.html', {'review_form': form})

@require_POST
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return HttpResponseForbidden()
    product_id = review.product.id
    review.delete()
    return redirect('product_detail', product_id=product_id)