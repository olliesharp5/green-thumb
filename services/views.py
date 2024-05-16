from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from profiles.models import UserProfile
from .models import Service, ServiceRequest, GardenerFeedback
from .forms import GardenerFeedbackForm

# Create your views here.
def services(request):
    """ A view to return the services page """
    gardeners = UserProfile.objects.filter(role='GR')
    context = {
        'gardeners': gardeners,
    }
    return render(request, "services/services.html", context)

def gardener_profile(request, username):
    gardener = get_object_or_404(UserProfile, user__username=username, role='GR')
    feedbacks = GardenerFeedback.objects.filter(gardener=gardener)
    context = {
        'gardener': gardener,
        'feedbacks': feedbacks,
    }
    return render(request, 'services/gardener_profile.html', context)

def gardener_feedback(request):
    if request.method == 'POST':
        form = GardenerFeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save()
            messages.success(request, f'Thank you for submitting feedback for {feedback.gardener.display_name}')
            return redirect('services')
    else:
        form = GardenerFeedbackForm()
    return render(request, 'gardener_feedback.html', {'form': form})

def service_request(request):
    services = Service.objects.all()
    if request.method == 'POST':
        full_name = request.POST['full_name']
        email = request.POST['email']
        selected_services = request.POST.getlist('services')
        message = request.POST['message']
        date_required = request.POST['date_required']
        files = request.FILES.getlist('file_upload')

        service_objects = Service.objects.filter(id__in=selected_services)

        if request.user.is_authenticated:
            service_request = ServiceRequest(full_name=full_name, email=email, message=message, date_required=date_required, user=request.user)
        else:
            service_request = ServiceRequest(full_name=full_name, email=email, message=message, date_required=date_required)

        service_request.save()

        for service in service_objects:
            service_request.services.add(service)

        for file in files:
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            service_request.file_upload = fs.url(filename)
            service_request.save()

        # Prepare email
        email_subject = render_to_string(
        'services/confirmation_emails/confirmation_email_subject.txt',
        {'service_request': service_request}
        )
        email_body = render_to_string(
        'services/confirmation_emails/confirmation_email_body.txt',
        {'service_request': service_request, 'contact_email': settings.DEFAULT_FROM_EMAIL, 'services': service_objects}
        )

        # Send confirmation email
        send_mail(
            email_subject,
            email_body,
            settings.DEFAULT_FROM_EMAIL,
            [email]
        )

        messages.success(request, f'Your service request has been submitted. A confirmation email has been sent to {email}.')
        return redirect('services')

    else:
        return render(request, 'services/service_request.html', {'services': services, 'user': request.user})