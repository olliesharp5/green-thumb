from django.shortcuts import render

from profiles.models import UserProfile

# Create your views here.
def services(request):
    """ A view to return the services page """
    gardeners = UserProfile.objects.filter(role='GR')
    context = {
        'gardeners': gardeners,
    }
    return render(request, "services/services.html", context)