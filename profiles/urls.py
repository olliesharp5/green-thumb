from django.urls import path

from .views import delete_profile
from . import views

app_name = 'profiles'

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('profile/order_history/', views.order_history, name='order_history'),
    path('profile/wishlist/', views.wishlist, name='wishlist'),
    path('profile/customer_service_requests/', views.customer_service_requests, name='customer_service_requests'),
    path('profile/service_requests/', views.service_requests, name='service_requests'),
    path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/<str:from_page>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('delete_profile/', delete_profile, name='delete_profile'),
]