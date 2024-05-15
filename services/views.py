from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage

from profiles.models import UserProfile
from .models import Service, ServiceRequest

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
    context = {
        'gardener': gardener,
    }
    return render(request, 'services/gardener_profile.html', context)

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

        messages.success(request, 'Your service request has been submitted.')
        return redirect('services')

    else:
        return render(request, 'services/service_request.html', {'services': services, 'user': request.user})