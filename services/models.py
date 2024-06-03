from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

from profiles.models import UserProfile


class Service(models.Model):
    """
    This is a Service model that represents different types of services offered.

    Attributes:
    SERVICE_CHOICES (list): A list of tuples defining the available service choices.
    name (CharField): The name of the service, chosen from SERVICE_CHOICES.

    Methods:
    __str__(): Returns a readable string representation of the Service object.
    """

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
    """
    This is a ServiceRequest model that represents a customer's request for services.

    Attributes:
    STATUS_CHOICES (list): A list of tuples defining the status choices for the service request.
    full_name (CharField): The full name of the person submitting the service request.
    email (EmailField): The email address of the person submitting the service request.
    services (ManyToManyField): The services requested by the customer.
    message (TextField): An optional message from the customer.
    file_upload (FileField): An optional file uploaded with the service request, stored in the 'uploads/' directory.
    date_required (DateField): The date when the service is required.
    created_at (DateTimeField): The date and time when the service request was created, automatically set on creation.
    status (CharField): The status of the service request, chosen from STATUS_CHOICES, with 'Open' as default.
    user (ForeignKey): The user who submitted the service request, can be null.

    Methods:
    __str__(): Returns a readable string representation of the ServiceRequest object.
    """

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


class GardenerFeedback(models.Model):
    """
    This is a GardenerFeedback model that represents feedback for gardeners.

    Attributes:
    gardener (ForeignKey): The gardener (user profile) receiving the feedback, limited to users with the 'Gardener' role.
    first_name (CharField): The first name of the person providing the feedback.
    title (CharField): The title of the feedback.
    message (TextField): The message content of the feedback.
    rating (DecimalField): The rating given, must be between 0 and 5.
    created_at (DateTimeField): The date and time when the feedback was created, automatically set on creation.

    Methods:
    __str__(): Returns a readable string representation of the GardenerFeedback object.
    """
    
    gardener = models.ForeignKey(UserProfile, on_delete=models.CASCADE, limit_choices_to={'role': 'GR'})
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    message = models.TextField()
    rating = models.DecimalField(max_digits=2, decimal_places=1, validators=[MinValueValidator(0), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback submitted by {self.user}"