from django.shortcuts import render

# Create your views here.
def bag_view(request):
    """ A view to return the bag.html page """
    return render(request, "bag/bag.html")