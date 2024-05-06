from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_view, name='cart_view')
]