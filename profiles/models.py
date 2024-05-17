from django.db import models
from django.apps import apps
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.db.models import Avg

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
    profile_image = models.ImageField(null=True, blank=True)
    about = models.TextField()

    default_phone_number = models.CharField(max_length=20, null=True, blank=True)
    default_street_address1 = models.CharField(max_length=80, null=True, blank=True)
    default_street_address2 = models.CharField(max_length=80, null=True, blank=True)
    default_town_or_city = models.CharField(max_length=40, null=True, blank=True)
    default_county = models.CharField(max_length=80, null=True, blank=True)
    default_postcode = models.CharField(max_length=20, null=True, blank=True)
    default_country = CountryField(blank_label='Country', null=True, blank=True)

    @property
    def calculate_rating(self):
        GardenerFeedback = apps.get_model('services', 'GardenerFeedback')
        reviews = GardenerFeedback.objects.filter(gardener=self)
        return round(reviews.aggregate(Avg('rating'))['rating__avg'] or 0.0, 1)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if self.role == 'GR':
            if not all([self.display_name, self.location, self.about]):
                raise ValueError("Gardener must have a display name, location, and about section.")
        super().save(*args, **kwargs)

class Wishlist(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)

    def __str__(self):
        return self.user.user.username