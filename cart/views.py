from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from products.models import Product

# Create your views here.
def cart_view(request):
    """ A view to return the cart.html page """
    return render(request, "cart/cart.html")


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    quantity = int(request.POST.get('quantity'))
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + quantity
    request.session['cart'] = cart
    
    return redirect('product_detail', product_id=product_id)