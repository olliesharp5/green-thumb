from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactRequest

def contact(request):
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

        messages.success(request, 'Your contact request has been submitted. View your requests in "My Profile"')
        return redirect('contact')

    return render(request, "contact/contact.html")