from django.shortcuts import render

# Create your views here.
def services(request):
    """ A view to return the services page """
    return render(request, "services/services.html")