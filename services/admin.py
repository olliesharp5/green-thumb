from django.contrib import admin
from .models import Service, ServiceRequest

# Register your models here.
admin.site.register(Service)
admin.site.register(ServiceRequest)