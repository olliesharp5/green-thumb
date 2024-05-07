from django.db import models

# Create your models here.

SUBJECT_CHOICES = [
    ('order_status', "Where's my order?"),
    ('report_issue', 'Report an issue'),
    ('product_question', 'Product question'),
    ('order_change', 'Cancel or amend order'),
    ('other', 'Other'),
]

class ContactRequest(models.Model):
   
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=200, choices=SUBJECT_CHOICES)
    message = models.TextField()
    file_upload = models.FileField(upload_to='', null=True, blank=True)  # upload_to is now blank
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Contact request from {self.full_name}"