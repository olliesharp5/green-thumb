from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import ContactRequest

def contact(request):
    """
    Handles the contact form submission and renders the contact page. If the user is authenticated, 
    pre-fills the form with their details.

    **Context**

    ``user_details``
    A dictionary containing the authenticated user's full name and email.

    ``full_name``
    The full name of the user submitting the contact form.

    ``email``
    The email address of the user submitting the contact form.

    ``subject``
    The subject of the contact request.

    ``message``
    The message body of the contact request.

    ``file_upload``
    An optional file upload associated with the contact request.

    **Methods**

    ``contact(request)``
    Handles both GET and POST requests. On POST, it processes the contact form, saves the contact 
    request to the database, sends a confirmation email, and redirects to the home page with a success 
    message. On GET, it renders the contact page with the user's details if authenticated.

    **Template:**

    :template:`contact/contact.html`
    """
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
        request.session['cart_changed'] = False
        messages.success(request, f'Your contact request has been submitted. A confirmation email has been sent to {email}.')
        return redirect('home')

    return render(request, "contact/contact.html", {'user_details': user_details})
