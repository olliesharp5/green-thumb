# Generated by Django 5.0.4 on 2024-05-12 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_alter_product_rating_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='title',
            field=models.CharField(max_length=200, null=True),
        ),
    ]