from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
]