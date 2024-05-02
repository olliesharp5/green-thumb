from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
]