import uuid

from django.db import models
from django.db.models import Sum
from django.conf import settings
from django_countries.fields import CountryField

from products.models import Product
from profiles.models import UserProfile


class Order(models.Model):
    """
    This is an Order model that represents a customer's order.

    Attributes:
    order_number (UUIDField): The unique identifier for the order, generated automatically.
    user_profile (ForeignKey): The user's profile associated with the order, can be null or blank.
    full_name (CharField): The full name of the person who placed the order.
    email (EmailField): The email address of the person who placed the order.
    phone_number (CharField): The phone number of the person who placed the order.
    country (CountryField): The country of the delivery address.
    postcode (CharField): The postal code of the delivery address, can be null or blank.
    town_or_city (CharField): The town or city of the delivery address.
    street_address1 (CharField): The first line of the street address.
    street_address2 (CharField): The second line of the street address, can be null or blank.
    county (CharField): The county of the delivery address, can be null or blank.
    date (DateTimeField): The date and time when the order was placed, automatically set on creation.
    delivery_cost (DecimalField): The cost of delivery for the order.
    order_total (DecimalField): The total cost of the items in the order.
    grand_total (DecimalField): The total cost of the order including delivery.
    original_cart (TextField): The original cart data as a JSON string.
    stripe_pid (CharField): The Stripe payment intent ID for the order.

    Methods:
    update_total(): Updates the grand total of the order, accounting for delivery costs.
    """
    order_number = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Automatically generates a new UUID when creating a new object.
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                     null=True, blank=True, related_name='orders')
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(blank_label='Country *', null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    original_cart = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default='')

    def update_total(self):
        """
        Update grand total each time a line item is added,
        accounting for delivery costs.
        """
        self.order_total = self.lineitems.aggregate(Sum('lineitem_total'))['lineitem_total__sum'] or 0
        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = self.order_total * settings.STANDARD_DELIVERY_PERCENTAGE / 100
        else:
            self.delivery_cost = 0
        self.grand_total = self.order_total + self.delivery_cost
        self.save()


class OrderLineItem(models.Model):
    """
    This is an OrderLineItem model that represents a single line item in an order.

    Attributes:
    order (ForeignKey): The order to which this line item belongs.
    product (ForeignKey): The product associated with this line item.
    product_size (CharField): The size of the product, can be null or blank.
    quantity (PositiveIntegerField): The quantity of the product in this line item.
    lineitem_total (DecimalField): The total cost of this line item, calculated based on product price and quantity.

    Methods:
    save(): Overrides the default save method to set the lineitem total and update the order total.
    __str__(): Returns a readable string representation of the OrderLineItem object.
    """
    order = models.ForeignKey(Order, null=False, blank=False, on_delete=models.CASCADE, related_name='lineitems')
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE)
    product_size = models.CharField(max_length=2, null=True, blank=True) # XS, S, M, L, XL
    quantity = models.PositiveIntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False)

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem total
        and update the order total.
        """
        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'SKU {self.product.sku} on order {self.order.order_number}'