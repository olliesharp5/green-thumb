from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from profiles.models import UserProfile
from .models import Service, ServiceRequest, GardenerFeedback
from .forms import GardenerFeedbackForm

def services(request):
    """
    A view to return the services page.

    **Context**

    ``gardeners``
    A queryset of `UserProfile` objects with the role 'GR' (gardeners).

    **Methods**

    ``services(request)``
    Handles GET requests to display the services page with a list of gardeners.

    **Template:**

    :template:`services/services.html`
    """
    gardeners = UserProfile.objects.filter(role='GR')
    context = {
        'gardeners': gardeners,
    }
    return render(request, "services/services.html", context)


def gardener_profile(request, username):
    """
    Displays the profile of a specific gardener and their feedback.

    **Context**

    ``gardener``
    The gardener's profile object, retrieved by their username.

    ``feedbacks``
    A queryset of feedbacks associated with the gardener.

    **Methods**

    ``gardener_profile(request, username)``
    Handles GET requests to display the gardener's profile page, including feedback.

    **Template:**

    :template:`services/gardener_profile.html`
    """
    gardener = get_object_or_404(UserProfile, user__username=username, role='GR')
    feedbacks = GardenerFeedback.objects.filter(gardener=gardener)
    context = {
        'gardener': gardener,
        'feedbacks': feedbacks,
    }
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user == gardener.user:
            feedback_form = GardenerFeedbackForm()
            context['feedback_form'] = feedback_form
    return render(request, 'services/gardener_profile.html', context)


def gardener_feedback(request):
    """
    Handles the submission of feedback for a gardener.

    **Context**

    ``form``
    An instance of `GardenerFeedbackForm` to handle feedback data input.

    **Methods**

    ``gardener_feedback(request)``
    Handles both GET and POST requests. On POST, it processes the feedback form and saves the feedback to the database.
    On GET, it renders the form for submitting feedback.

    **Template:**

    :template:`services/gardener_feedback.html`
    """
    if request.method == 'POST':
        form = GardenerFeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user  # Associate the feedback with the logged-in user
            feedback.save()
            request.session['cart_changed'] = False
            messages.success(request, f'Thank you for submitting feedback for {feedback.gardener.display_name}')
            return redirect('gardener_profile', username=feedback.gardener.user.username)
    else:
        form = GardenerFeedbackForm()
    return render(request, 'services/gardener_feedback.html', {'form': form})


def update_gardener_feedback(request, feedback_id):
    feedback = get_object_or_404(GardenerFeedback, id=feedback_id)
    if request.user != feedback.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = GardenerFeedbackForm(request.POST, instance=feedback)
        if form.is_valid():
            form.save()
            messages.success(request, 'Feedback updated successfully')
            return redirect('gardener_profile', username=feedback.gardener.user.username)
    else:
        form = GardenerFeedbackForm(instance=feedback)

    return render(request, 'services/update_gardener_feedback.html', {'form': form, 'feedback': feedback})


@require_POST
def delete_gardener_feedback(request, feedback_id):
    feedback = get_object_or_404(GardenerFeedback, id=feedback_id)
    if request.user != feedback.user and not request.user.is_superuser:
        return HttpResponseForbidden()
    feedback.delete()
    messages.success(request, 'Feedback deleted successfully')
    return redirect('gardener_profile', username=feedback.gardener.user.username)


def service_request(request):
    """
    Handles the submission of a service request.

    **Context**

    ``services``
    A queryset of all available `Service` objects.

    ``full_name``
    The full name of the user submitting the service request.

    ``email``
    The email address of the user submitting the service request.

    ``selected_services``
    The list of selected services for the service request.

    ``message``
    The message body of the service request.

    ``date_required``
    The date the service is required.

    ``files``
    A list of files uploaded with the service request.

    ``service_objects``
    A queryset of `Service` objects matching the selected services.

    ``service_request``
    The service request object created from the form data.

    **Methods**

    ``service_request(request)``
    Handles both GET and POST requests. On POST, it processes the service request form, saves the request to the database,
    handles file uploads, and sends a confirmation email. On GET, it renders the form for submitting a service request.

    **Template:**

    :template:`services/service_request.html`
    """
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

        request.session['cart_changed'] = False
        messages.success(request, f'Your service request has been submitted. A confirmation email has been sent to {email}.')
        return redirect('services')

    else:
        return render(request, 'services/service_request.html', {'services': services, 'user': request.user})
