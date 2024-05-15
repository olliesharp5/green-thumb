from django.urls import path

from .views import delete_profile
from . import views

app_name = 'profiles'

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/<str:from_page>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('delete_profile/', delete_profile, name='delete_profile'),
]