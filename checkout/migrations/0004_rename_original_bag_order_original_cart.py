# Generated by Django 5.0.4 on 2024-05-10 14:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0003_order_original_bag_order_stripe_pid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='original_bag',
            new_name='original_cart',
        ),
    ]