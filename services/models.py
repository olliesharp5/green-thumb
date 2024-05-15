from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Service(models.Model):
    SERVICE_CHOICES = [
        ('gardening', "Gardening"),
        ('lawn_care', 'Lawn Care'),
        ('holiday_service', 'Holiday Service'),
        ('seasonal_care', 'Seasonal Care'),
    ]

    name = models.CharField(max_length=200, choices=SERVICE_CHOICES)

    def __str__(self):
        return self.name

class ServiceRequest(models.Model):
    STATUS_CHOICES = [
        ('O', 'Open'),
        ('P', 'In Progress'),
        ('C', 'Closed'),
    ]

    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    services = models.ManyToManyField(Service)
    message = models.TextField(null=True, blank=True)
    file_upload = models.FileField(upload_to='uploads/', null=True, blank=True)
    date_required = models.DateField(help_text='Date when the service is required')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='O')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return f"Service request from {self.full_name}"