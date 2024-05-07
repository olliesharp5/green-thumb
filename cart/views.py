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
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    cart = request.session.get('cart', {})

    if size:
        if str(product_id) in list(cart.keys()):
            if size in cart[str(product_id)]['items_by_size'].keys():
                cart[str(product_id)]['items_by_size'][size] += quantity
            else:
                cart[str(product_id)]['items_by_size'][size] = quantity
        else:
            cart[str(product_id)] = {'items_by_size': {size: quantity}}
    else:
        if str(product_id) in list(cart.keys()):
            cart[str(product_id)] += quantity
        else:
            cart[str(product_id)] = quantity

    request.session['cart'] = cart
    return redirect('product_detail', product_id=product_id)


def update_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    quantity = int(request.POST.get('quantity'))
    size = str(request.POST.get('size'))  # Convert size to string
    cart = request.session.get('cart', {})

    if str(product_id) in list(cart.keys()):
        if isinstance(cart[str(product_id)], dict) and 'items_by_size' in cart[str(product_id)]:
            if size in cart[str(product_id)]['items_by_size']:
                cart[str(product_id)]['items_by_size'][size] = quantity
        else:
            cart[str(product_id)] = quantity

    request.session['cart'] = cart
    return redirect('cart_view')


def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    size = request.POST.get('size')
    cart = request.session.get('cart', {})

    if str(product_id) in list(cart.keys()):
        if isinstance(cart[str(product_id)], dict) and 'items_by_size' in cart[str(product_id)]:
            if size in cart[str(product_id)]['items_by_size']:
                del cart[str(product_id)]['items_by_size'][size]
                # If there are no other sizes for this product, remove the product entry
                if not cart[str(product_id)]['items_by_size']:
                    del cart[str(product_id)]
        else:
            del cart[str(product_id)]

    request.session['cart'] = cart
    return redirect('cart_view')