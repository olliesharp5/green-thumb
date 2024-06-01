from django.db import models
from django.apps import apps
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.db.models import Avg

from products.models import Product


class UserProfile(models.Model):
    """
    This is a UserProfile model that represents an extended user profile.

    Attributes:
    USER_ROLES (tuple): A tuple constant that defines the possible roles ('RU', 'Regular User') and ('GR', 'Gardener').
    user (OneToOneField): A one-to-one relationship with the User model; on user deletion, the associated profile will also be deleted.
    role (CharField): The role of the user within the application. Choices are defined in the USER_ROLES constant, with 'Regular User' as default.
    display_name (CharField): The displayed name for the user in the system. It can be null, blank, and unique with a maximum of 100 characters.
    location (TextField): The recorded location for the user.
    profile_image (ImageField): The profile image of the user, can be null or blank.
    about (TextField): A text describing about the user.

    default_phone_number (CharField): The default phone number for the user, can be null or blank.
    default_street_address1 (CharField): The first line of the default street address, can be null or blank.
    default_street_address2 (CharField): The second line of the default street address, can be null or blank.
    default_town_or_city (CharField): The default town or city, can be null or blank.
    default_county (CharField): The default county, can be null or blank.
    default_postcode (CharField): The default postal code, can be null or blank.
    default_country (CountryField): The default country, can be null or blank.

    Methods:
    calculate_rating(): Calculates and returns the average rating for the gardener from the GardenerFeedback model.
    __str__(): Returns a readable string representation of the UserProfile object.
    save(): Overrides the default save method to enforce validation rules for gardeners.
    """
    
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
    """
    This is a Wishlist model that represents a user's wishlist.

    Attributes:
    user (ForeignKey): The user profile associated with the wishlist.
    products (ManyToManyField): The products included in the user's wishlist.

    Methods:
    __str__(): Returns a readable string representation of the Wishlist object, indicating the username of the user.
    """
    
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)

    def __str__(self):
        return self.user.user.username