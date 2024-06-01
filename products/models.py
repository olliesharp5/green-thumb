from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg
from django.core.validators import MaxValueValidator, MinValueValidator
from django.template.defaultfilters import slugify

class Category(models.Model):
    """
    This is a Category model that represents a product category.

    Attributes:
    name (CharField): The name of the category.
    slug (SlugField): The URL-friendly representation of the category name, unique.
    parent (ForeignKey): The parent category for hierarchical organization, can be null or blank.

    Methods:
    save(): Overrides the default save method to automatically set the slug based on the category name if not provided.
    __str__(): Returns a readable string representation of the Category object.
    """

    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    """
    This is a Product model that represents a product.

    Attributes:
    sku (CharField): The SKU of the product, can be null or blank.
    name (CharField): The name of the product.
    description (TextField): The description of the product.
    has_size (BooleanField): Indicates if the product has sizes, can be null or blank.
    price (DecimalField): The price of the product.
    rating (DecimalField): The average rating of the product, can be null or blank.
    image (ImageField): The image of the product, can be null or blank.
    category (ForeignKey): The category to which the product belongs.
    date_added (DateTimeField): The date and time when the product was added, automatically set on creation.

    Methods:
    calculate_rating(): Calculates and returns the average rating of the product based on its reviews.
    __str__(): Returns a readable string representation of the Product object.
    """

    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    has_size = models.BooleanField(default=False, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def calculate_rating(self):
        reviews = self.reviews.all()
        return round(reviews.aggregate(Avg('rating'))['rating__avg'] or 0.0, 1)

    def __str__(self):
        return self.name

class Review(models.Model):
    """
    This is a Review model that represents a product review.

    Attributes:
    product (ForeignKey): The product being reviewed.
    user (ForeignKey): The user who wrote the review.
    title (CharField): The title of the review, can be null.
    rating (DecimalField): The rating given by the user, must be between 0 and 5.
    text (TextField): The text content of the review.
    date_added (DateTimeField): The date and time when the review was added, automatically set on creation.

    Methods:
    __str__(): Returns a readable string representation of the Review object.
    """
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, validators=[MinValueValidator(0), MaxValueValidator(5)])
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)