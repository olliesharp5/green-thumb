from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from checkout.models import Order
from products.models import Product

from contact.models import ContactRequest
from .models import UserProfile, Wishlist
from .forms import UserForm, UserProfileForm, GardenerProfileForm

# Create your views here.

@login_required
def profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    contact_requests = ContactRequest.objects.filter(email=request.user.email)
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
    wishlist = Wishlist.objects.get(user=user_profile)
    orders = Order.objects.filter(user_profile=user_profile)
    context = {
        'user_form': user_form,
        'user_profile_form': user_profile_form,
        'gardener_profile_form': gardener_profile_form, 
        'wishlist': wishlist,
        'orders': orders,
        'user_profile': user_profile,
        'contact_requests': contact_requests,
    }
    return render(request, 'profiles/profile.html', context)

    
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    user_profile = UserProfile.objects.get(user=request.user)
    wishlist, created = Wishlist.objects.get_or_create(user=user_profile)
    wishlist.products.add(product)
    return redirect('product_detail', product_id=product.id)

def remove_from_wishlist(request, product_id, from_page):
    product = get_object_or_404(Product, pk=product_id)
    user_profile = UserProfile.objects.get(user=request.user)
    wishlist, created = Wishlist.objects.get_or_create(user=user_profile)
    wishlist.products.remove(product)
    if from_page == 'profile':
        return redirect('profiles:profile')
    else:
        return redirect('product_detail', product_id=product.id)