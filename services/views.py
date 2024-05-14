from django.shortcuts import render, get_object_or_404

from profiles.models import UserProfile

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