from django.shortcuts import render

# Create your views here.
def cart_view(request):
    """ A view to return the cart.html page """
    return render(request, "cart/cart.html")