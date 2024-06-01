from django.contrib import admin
from django.urls import path

from . import views


urlpatterns = [
    path('', views.services, name='services'),
    path('gardener/<str:username>/', views.gardener_profile, name='gardener_profile'),
    path('gardener_feedback/', views.gardener_feedback, name='gardener_feedback'),
    path('service_request/', views.service_request, name='service_request'),
]
