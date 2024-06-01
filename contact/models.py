from django.db import models

SUBJECT_CHOICES = [
    ('order_status', "Where's my order?"),
    ('report_issue', 'Report an issue'),
    ('product_question', 'Product question'),
    ('order_change', 'Cancel or amend order'),
    ('other', 'Other'),
]

STATUS_CHOICES = [
        ('O', 'Open'),
        ('P', 'In Progress'),
        ('C', 'Closed'),
    ]

class ContactRequest(models.Model):
    """
    This is a ContactRequest model that represents a customer's contact request.

    Attributes:
    full_name (CharField): The full name of the person submitting the contact request.
    email (EmailField): The email address of the person submitting the contact request.
    subject (CharField): The subject of the contact request, choices are defined in SUBJECT_CHOICES.
    message (TextField): The message content of the contact request.
    file_upload (FileField): An optional file uploaded with the contact request, stored in the 'uploads/' directory.
    created_at (DateTimeField): The date and time when the contact request was created, automatically set on creation.
    status (CharField): The status of the contact request, choices are defined in STATUS_CHOICES, with 'Open' as default.

    Methods:
    __str__(): Returns a readable string representation of the ContactRequest object.
    """
    
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=200, choices=SUBJECT_CHOICES)
    message = models.TextField()
    file_upload = models.FileField(upload_to='uploads/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='O')
    
    def __str__(self):
        return f"Contact request from {self.full_name}"