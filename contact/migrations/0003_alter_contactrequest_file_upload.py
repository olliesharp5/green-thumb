# Generated by Django 5.0.4 on 2024-05-14 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0002_contactrequest_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactrequest',
            name='file_upload',
            field=models.FileField(blank=True, null=True, upload_to='uploads/'),
        ),
    ]
