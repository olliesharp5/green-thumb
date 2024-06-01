from django.contrib import admin

from .models import Service, ServiceRequest, GardenerFeedback


admin.site.register(Service)
admin.site.register(ServiceRequest)
admin.site.register(GardenerFeedback)