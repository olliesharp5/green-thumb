from django.shortcuts import render, get_object_or_404, redirect
from django.db.models.functions import Coalesce
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.db.models import Q, Count, Avg, Value, DecimalField
from django.views.decorators.http import require_POST
from profiles.models import Wishlist, UserProfile
from .models import Product, Category, Review
from .forms import SortForm, ProductForm, ReviewForm


def all_products(request):
    """
    Retrieves and displays all products, optionally filtered by a search query and sorted by a specified criterion.

    **Context**

    ``query``
    The search query entered by the user.

    ``sort_by``
    The field by which to sort the products.

    ``sort_options``
    A mapping of sort option names to actual model field names.

    ``products``
    A queryset of products filtered and sorted based on the search query and sort criterion.

    ``form``
    An instance of `SortForm` pre-filled with the current GET parameters.

    **Methods**

    ``all_products(request)``
    Handles GET requests to display the products page with filtering and sorting options.

    **Template:**

    :template:`products/products.html`
    """
    query = request.GET.get('q', '').strip()
    sort_by = request.GET.get('sort_by', 'name')

    sort_options = {
        'recent': '-date_added',
        'highest_rating': '-coalesced_rating',
        'best_selling': '-sales_count',
        'price': 'price',
        '-price': '-price',
        'name': 'name'
    }
    sort_by = sort_options.get(sort_by, 'name')

    if 'q' in request.GET and not query:
        messages.error(request, 'Please enter a search term.')

    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()

    products = products.annotate(
        sales_count=Count('orderlineitem'),
        coalesced_rating=Coalesce('rating', Value(0), output_field=DecimalField())
    ).order_by(sort_by)
    
    paginator = Paginator(products, 9)  # 9 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    form = SortForm(request.GET)
    return render(request, 'products/products.html', {'page_obj': page_obj, 'form': form})

def products_by_category(request, category_slug):
    """
    Retrieves and displays products belonging to a specified category and its subcategories.

    **Context**

    ``sort_by``
    The field by which to sort the products, mapped to actual model fields or annotated fields.

    ``category``
    The main category specified by the slug.

    ``subcategories``
    A queryset of subcategories under the main category.

    ``products``
    A queryset of products filtered by the main category and its subcategories, annotated with average rating and sales count, and sorted based on the specified criterion.

    ``form``
    An instance of `SortForm` pre-filled with the current GET parameters.

    **Methods**

    ``products_by_category(request, category_slug)``
    Handles GET requests to display products belonging to a specified category and its subcategories.

    **Template:**

    :template:`products/products.html`
    """
    sort_options = {
        'recent': '-date_added',
        'highest_rating': '-avg_coalesced_rating',
        'best_selling': '-sales_count',
        'price': 'price',
        '-price': '-price',
        'name': 'name'
    }
    
    sort_by = request.GET.get('sort_by', 'name')
    sort_by = sort_options.get(sort_by, 'name')

    category = get_object_or_404(Category, slug=category_slug)
    subcategories = Category.objects.filter(parent=category)

    products = Product.objects.filter(
        Q(category=category) | Q(category__in=subcategories)
    ).annotate(
        avg_rating=Avg('reviews__rating'),
        avg_coalesced_rating=Coalesce(Avg('reviews__rating'), Value(0), output_field=DecimalField()),
        sales_count=Count('orderlineitem')
    ).order_by(sort_by)
    
    paginator = Paginator(products, 9)  # 9 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    form = SortForm(request.GET)
    return render(request, 'products/products.html', {'page_obj': page_obj, 'category_name': category.name, 'category': category, 'form': form})


def product_detail(request, product_id):
    """
    Retrieves and displays the details of a specified product, including its reviews and user's wishlist status.

    **Context**

    ``product``
    The product object retrieved by its ID.

    ``reviews``
    A queryset of reviews for the product.

    ``user_has_reviewed``
    A flag indicating whether the authenticated user has reviewed the product.

    ``wishlist``
    The wishlist of the authenticated user, if any.

    ``form``
    An instance of `ProductForm` pre-filled with the product data for superusers.

    ``review_form``
    An instance of `ReviewForm` pre-filled with the user's review if it exists, otherwise empty.

    **Methods**

    ``product_detail(request, product_id)``
    Handles GET requests to display the product details page, including reviews and review forms.

    **Template:**

    :template:`products/product_detail.html`
    """
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
            review_form = ReviewForm(instance=review)
            context['review'] = review  # Add review to context only if it exists
            user_has_reviewed = True
        except Review.DoesNotExist:
            review_form = ReviewForm()
            context['review'] = None  # Ensure review is set to None if it doesn't exist
        context['review_form'] = review_form
    else:
        review_form = ReviewForm()
        context['review_form'] = review_form
        context['review'] = None  # Ensure review is set to None if user is not authenticated
    context['user_has_reviewed'] = user_has_reviewed
    return render(request, 'products/product_detail.html', context)


def add_product(request):
    """
    Handles the addition of a new product by displaying and processing the product form.

    **Context**

    ``form``
    An instance of `ProductForm` to handle product data input.

    **Methods**

    ``add_product(request)``
    Handles both GET and POST requests. On POST, it processes the product form and saves the product to the database.
    On GET, it renders the form for adding a new product.

    **Template:**

    :template:`products/add_product.html`
    """
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            request.session['cart_changed'] = False
            messages.success(request, 'The advert has been added to your site.')
            return redirect('home')
    else:
        form = ProductForm()
    return render(request, 'products/add_product.html', {'form': form})


def edit_product(request, product_id):
    """
    Handles the editing of an existing product by displaying and processing the product form.

    **Context**

    ``product``
    The product object to be edited, retrieved by its ID.

    ``form``
    An instance of `ProductForm` pre-filled with the product data.

    **Methods**

    ``edit_product(request, product_id)``
    Handles both GET and POST requests. On POST, it processes the product form and updates the product in the database.
    On GET, it renders the form for editing the product. Only accessible by superusers.

    **Template:**

    :template:`products/edit_product.html`
    """
    if not request.user.is_superuser:
        messages.error(request, 'Only superusers can edit products.')
        return redirect('home')

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()
            request.session['cart_changed'] = False
            messages.success(request, f'Successfully updated product {product.name}!')
            return redirect('product_detail', product_id=product.id)
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/edit_product.html', {'form': form})


def delete_product(request, product_id):
    """
    Handles the deletion of a product and its removal from any carts.

    **Context**

    ``product``
    The product object to be deleted, retrieved by its ID.

    ``cart``
    The current state of the shopping cart stored in the session.

    **Methods**

    ``delete_product(request, product_id)``
    Handles POST requests to delete the product from the database and remove it from any shopping carts. 

    **Template:**

    :template:`redirect to the home page`
    """
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
    """
    Handles the creation of a new review for a specified product.

    **Context**

    ``form``
    An instance of `ReviewForm` to handle review data input.

    **Methods**

    ``create_review(request, product_id)``
    Handles both GET and POST requests. On POST, it processes the review form and saves the review to the database.
    On GET, it renders the form for adding a new review.

    **Template:**

    :template:`reviews/create_review.html`
    """
    if request.method == 'POST':
        form = ReviewForm(request.POST)
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
    """
    Handles the updating of an existing review.

    **Context**

    ``review``
    The review object to be updated, retrieved by its ID.

    ``form``
    An instance of `ReviewForm` pre-filled with the review data.

    **Methods**

    ``update_review(request, review_id)``
    Handles both GET and POST requests. On POST, it processes the review form and updates the review in the database.
    On GET, it redirects to the product detail page. Only accessible by the review's owner.

    **Template:**

    :template:`redirect to the product detail page`
    """
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return HttpResponseForbidden()
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('product_detail', product_id=review.product.id)
    else:
        form = ReviewForm(instance=review)
    
    return render(request, 'products/update_review.html', {'form': form, 'review': review})


@require_POST
def delete_review(request, review_id):
    """
    Handles the deletion of a review.

    **Context**

    ``review``
    The review object to be deleted, retrieved by its ID.

    ``product_id``
    The ID of the product associated with the review.

    **Methods**

    ``delete_review(request, review_id)``
    Handles POST requests to delete the review from the database. Only accessible by the review's owner or superusers.

    **Template:**

    :template:`redirect to the product detail page`
    """
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user and not request.user.is_superuser:
        return HttpResponseForbidden()
    product_id = review.product.id
    review.delete()
    return redirect('product_detail', product_id=product_id)
