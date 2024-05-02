from django.shortcuts import render, get_object_or_404, redirect
from products.models import Product
from .models import UserProfile, Wishlist

# Create your views here.

def profile(request):
    return render(request, 'profiles/profile.html')

def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    user_profile = UserProfile.objects.get(user=request.user)
    wishlist, created = Wishlist.objects.get_or_create(user=user_profile)
    wishlist.products.add(product)
    return redirect('product_detail', product_id=product.id)

def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    user_profile = UserProfile.objects.get(user=request.user)
    wishlist, created = Wishlist.objects.get_or_create(user=user_profile)
    wishlist.products.remove(product)
    return redirect('product_detail', product_id=product.id)