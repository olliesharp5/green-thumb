from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from checkout.models import Order
from products.models import Product

from contact.models import ContactRequest
from services.models import ServiceRequest
from .models import UserProfile, Wishlist
from .forms import UserForm, UserProfileForm, GardenerProfileForm

@login_required
def profile(request):
    """
    Handles the display and update of the user's profile.

    **Context**

    ``user_profile``
    The user's profile object.

    ``user_form``
    An instance of `UserForm` for updating the user's basic information.

    ``user_profile_form``
    An instance of `UserProfileForm` for updating the user's profile information.

    ``gardener_profile_form``
    An instance of `GardenerProfileForm` for updating the gardener-specific profile information.

    **Methods**

    ``profile(request)``
    Handles both GET and POST requests. On POST, it processes the appropriate form based on the data submitted 
    and updates the user's profile. On GET, it renders the profile page with pre-filled forms.

    **Template:**

    :template:`profiles/profile.html`
    """
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        if 'first_name' in request.POST:
            user_form = UserForm(request.POST, instance=request.user)
            if user_form.has_changed() and user_form.is_valid():
                user_form.save()
        else:
            user_form = UserForm(instance=request.user)

        if 'default_phone_number' in request.POST:
            user_profile_form = UserProfileForm(request.POST, instance=user_profile)
            if user_profile_form.has_changed() and user_profile_form.is_valid():
                user_profile_form.save()
        else:
            user_profile_form = UserProfileForm(instance=user_profile)

        if 'display_name' in request.POST:
            gardener_profile_form = GardenerProfileForm(request.POST, request.FILES, instance=user_profile)
            if gardener_profile_form.has_changed() and gardener_profile_form.is_valid():
                gardener_profile_form.save()
        else:
            gardener_profile_form = GardenerProfileForm(instance=user_profile)
    else:
        user_form = UserForm(instance=request.user)
        user_profile_form = UserProfileForm(instance=user_profile)
        gardener_profile_form = GardenerProfileForm(instance=user_profile)

    context = {
        'user_form': user_form,
        'user_profile_form': user_profile_form,
        'gardener_profile_form': gardener_profile_form, 
        'user_profile': user_profile,
    }
    return render(request, 'profiles/profile.html', context)


@login_required
def order_history(request):
    """
    Displays the order history of the logged-in user.

    **Context**

    ``user_profile``
    The user's profile object.

    ``orders``
    A queryset of orders associated with the user's profile.

    **Methods**

    ``order_history(request)``
    Handles GET requests to display the user's order history.

    **Template:**

    :template:`profiles/order_history.html`
    """
    user_profile = UserProfile.objects.get(user=request.user)
    orders = Order.objects.filter(user_profile=user_profile)
    context = {
        'orders': orders,
        'user_profile': user_profile,
    }
    return render(request, 'profiles/order_history.html', context)


@login_required
def wishlist(request):
    """
    Displays the wishlist of the logged-in user.

    **Context**

    ``user_profile``
    The user's profile object.

    ``wishlist``
    The wishlist associated with the user's profile.

    **Methods**

    ``wishlist(request)``
    Handles GET requests to display the user's wishlist.

    **Template:**

    :template:`profiles/wishlist.html`
    """
    user_profile = UserProfile.objects.get(user=request.user)
    wishlist = Wishlist.objects.get(user=user_profile)
    context = {
        'wishlist': wishlist,
        'user_profile': user_profile,
    }
    return render(request, 'profiles/wishlist.html', context)


@login_required
def customer_service_requests(request):
    """
    Displays the customer's service requests.

    **Context**

    ``contact_requests``
    A queryset of contact requests associated with the user's email.

    **Methods**

    ``customer_service_requests(request)``
    Handles GET requests to display the user's customer service requests.

    **Template:**

    :template:`profiles/customer_service_requests.html`
    """
    contact_requests = ContactRequest.objects.filter(email=request.user.email)
    context = {
        'contact_requests': contact_requests,
    }
    return render(request, 'profiles/customer_service_requests.html', context)


@login_required
def service_requests(request):
    """
    Displays the service requests of the logged-in user.

    **Context**

    ``service_requests``
    A queryset of service requests associated with the user.

    **Methods**

    ``service_requests(request)``
    Handles GET requests to display the user's service requests.

    **Template:**

    :template:`profiles/service_requests.html`
    """
    service_requests = ServiceRequest.objects.filter(user=request.user)
    context = {
        'service_requests': service_requests,
    }
    return render(request, 'profiles/service_requests.html', context)


@login_required
def delete_profile(request):
    """
    Deletes the profile of the logged-in user and logs them out.

    **Context**

    ``user``
    The user object to be deleted.

    **Methods**

    ``delete_profile(request)``
    Handles POST requests to delete the user's profile and log them out. Redirects to the home page with a success message.

    **Template:**

    :template:`redirect to the home page`
    """
    user = request.user
    user.delete()
    logout(request)
    messages.success(request, 'User successfully deleted!')
    return redirect('home')


def add_to_wishlist(request, product_id):
    """
    Adds a product to the wishlist of the logged-in user.

    **Context**

    ``product``
    The product object to be added to the wishlist, retrieved by its ID.

    ``user_profile``
    The user's profile object.

    ``wishlist``
    The wishlist associated with the user's profile.

    **Methods**

    ``add_to_wishlist(request, product_id)``
    Handles POST requests to add the product to the user's wishlist. Redirects to the product detail page.

    **Template:**

    :template:`redirect to the product detail page`
    """
    product = get_object_or_404(Product, pk=product_id)
    user_profile = UserProfile.objects.get(user=request.user)
    wishlist, created = Wishlist.objects.get_or_create(user=user_profile)
    wishlist.products.add(product)
    return redirect('product_detail', product_id=product.id)


def remove_from_wishlist(request, product_id, from_page):
    """
    Removes a product from the wishlist of the logged-in user.

    **Context**

    ``product``
    The product object to be removed from the wishlist, retrieved by its ID.

    ``user_profile``
    The user's profile object.

    ``wishlist``
    The wishlist associated with the user's profile.

    **Methods**

    ``remove_from_wishlist(request, product_id, from_page)``
    Handles POST requests to remove the product from the user's wishlist. Redirects to the appropriate page based on the `from_page` parameter.

    **Template:**

    :template:`redirect to the profile or product detail page`
    """
    product = get_object_or_404(Product, pk=product_id)
    user_profile = UserProfile.objects.get(user=request.user)
    wishlist, created = Wishlist.objects.get_or_create(user=user_profile)
    wishlist.products.remove(product)
    if from_page == 'profile':
        return redirect('profiles:profile')
    else:
        return redirect('product_detail', product_id=product.id)
