from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField

from products.models import Product


# Create your models here.
class UserProfile(models.Model):
    
    USER_ROLES = (
        ('RU', 'Regular User'),
        ('GR', 'Gardener'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=2, choices=USER_ROLES, default='RU')
    display_name = models.CharField(max_length=100, null=True, blank=True, unique=True)
    location = models.TextField()
    # profile_image = CloudinaryField('profile_image', default='profile_placeholder')
    about = models.TextField()

    default_phone_number = models.CharField(max_length=20, null=True, blank=True)
    default_street_address1 = models.CharField(max_length=80, null=True, blank=True)
    default_street_address2 = models.CharField(max_length=80, null=True, blank=True)
    default_town_or_city = models.CharField(max_length=40, null=True, blank=True)
    default_county = models.CharField(max_length=80, null=True, blank=True)
    default_postcode = models.CharField(max_length=20, null=True, blank=True)
    default_country = CountryField(blank_label='Country', null=True, blank=True)

    def __str__(self):
        return self.user.username

class Wishlist(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)

    def __str__(self):
        return self.user.user.username