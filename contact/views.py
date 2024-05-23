from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import ContactRequest

def contact(request):
    user_details = {}
    if request.user.is_authenticated:
        user_details = {
            'full_name': request.user.get_full_name(),
            'email': request.user.email,
        }

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        file_upload = request.FILES.get('file_upload')

        contact_request = ContactRequest(
            full_name=full_name,
            email=email,
            subject=subject,
            message=message,
            file_upload=file_upload
        )
        contact_request.save()

        email_subject = render_to_string(
            'contact/confirmation_emails/confirmation_email_subject.txt',
            {'contact_request': contact_request}
        )
        email_body = render_to_string(
            'contact/confirmation_emails/confirmation_email_body.txt',
            {'contact_request': contact_request, 'contact_email': settings.DEFAULT_FROM_EMAIL}
        )

        send_mail(
            email_subject,
            email_body,
            settings.DEFAULT_FROM_EMAIL,
            [email]
        )

        messages.success(request, 'Your contact request has been submitted. A confirmation email has been sent to {email}.')
        return redirect('home')

    return render(request, "contact/contact.html", {'user_details': user_details})
