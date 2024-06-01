from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Review


# Triggers the calculate_rating method and updates the product's rating accordingly
@receiver([post_save, post_delete], sender=Review)
def update_product_rating(sender, instance, **kwargs):
    instance.product.rating = instance.product.calculate_rating()
    instance.product.save()