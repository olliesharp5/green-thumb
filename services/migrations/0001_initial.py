# Generated by Django 5.0.4 on 2024-05-15 14:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('gardening', 'Gardening'), ('lawn_care', 'Lawn Care'), ('holiday_service', 'Holiday Service'), ('seasonal_care', 'Seasonal Care')], max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField(blank=True, null=True)),
                ('file_upload', models.FileField(blank=True, null=True, upload_to='uploads/')),
                ('date_required', models.DateField(help_text='Date when the service is required')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('O', 'Open'), ('P', 'In Progress'), ('C', 'Closed')], default='O', max_length=2)),
                ('services', models.ManyToManyField(to='services.service')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
