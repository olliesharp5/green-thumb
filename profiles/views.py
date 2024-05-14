from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from checkout.models import Order
from products.models import Product
from .models import UserProfile, Wishlist
from .forms import UserForm, UserProfileForm

# Create your views here.

@login_required
def profile(request):
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
    else:
        user_form = UserForm(instance=request.user)
        user_profile_form = UserProfileForm(instance=user_profile)
    wishlist = Wishlist.objects.get(user=user_profile)
    orders = Order.objects.filter(user_profile=user_profile)
    context = {
        'user_form': user_form,
        'user_profile_form': user_profile_form,
        'wishlist': wishlist,
        'orders': orders,
        'user_profile': user_profile,
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


def gardener_profile(request, username):
    gardener = get_object_or_404(UserProfile, user__username=username, role='GR')
    context = {
        'gardener': gardener,
    }
    return render(request, 'profiles/gardener_profile.html', context)