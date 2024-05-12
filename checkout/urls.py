from django.urls import path
from . import views
from .webhooks import webhook

urlpatterns = [
    path('', views.checkout, name='checkout'),
    # First URL pattern will be used when both 'order_number' and 'source' arguments are provided
    # The second URL pattern will be used when only the 'order_number' argument is provided.
    path('checkout_success/<order_number>/<source>/', views.checkout_success, name='checkout_success'),
    path('checkout_success/<order_number>/', views.checkout_success, name='checkout_success'),
    path('cache_checkout_data/', views.cache_checkout_data, name='cache_checkout_data'),
    path('wh/', webhook, name='webhook'),
]