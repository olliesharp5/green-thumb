from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect

from products.models import Product

def cart_view(request):
    """
    Renders the cart page.

    **Context**

    ``cart_changed``
    A flag in the session indicating whether the cart has changed.

    **Template:**

    :template:`cart/cart.html`
    """
    request.session['cart_changed'] = False
    return render(request, "cart/cart.html")


def add_to_cart(request, product_id):
    """
    Adds a specified quantity of a product to the shopping cart. If the product has 
    a size option, the size is also taken into account.

    **Context**

    ``product_id``
    The ID of the product to be added to the cart.

    ``cart``
    The current state of the shopping cart stored in the session.

    ``quantity``
    The quantity of the product to be added.

    ``size``
    The size of the product, if applicable.

    **Methods**

    ``add_to_cart(request, product_id)``
    Handles the logic for adding a product to the cart and updating the session 
    accordingly. Also manages success messages for user feedback.

    **Template:**

    :template:`redirect or HttpResponseRedirect to the referring page`
    """
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
                messages.success(request, f'Quantity of {product.name} size {size} in your cart has been updated!')
            else:
                cart[str(product_id)]['items_by_size'][size] = quantity
                messages.success(request, f'{product.name} size {size} has been added to your cart!')
        else:
            cart[str(product_id)] = {'items_by_size': {size: quantity}}
            messages.success(request, f'{product.name} size {size} has been added to your cart!')
    else:
        if str(product_id) in list(cart.keys()):
            cart[str(product_id)] += quantity
            messages.success(request, f'Quantity of {product.name} in your cart has been updated!')
        else:
            cart[str(product_id)] = quantity
            messages.success(request, f'{product.name} has been added to your cart!')

    request.session['cart'] = cart
    request.session['cart_changed'] = True
    if request.POST.get('from_product_page') == 'true':
        return redirect('product_detail', product_id=product_id)
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def update_cart(request, product_id):
    """
    Updates the quantity of a specified product in the shopping cart. If the product 
    has a size option, the size is also taken into account.

    **Context**

    ``product_id``
    The ID of the product to be updated in the cart.

    ``cart``
    The current state of the shopping cart stored in the session.

    ``quantity``
    The new quantity of the product.

    ``size``
    The size of the product, if applicable.

    **Methods**

    ``update_cart(request, product_id)``
    Handles the logic for updating a product's quantity in the cart and updating the 
    session accordingly. Also manages success messages for user feedback.

    **Template:**

    :template:`redirect to the cart view`
    """
    product = get_object_or_404(Product, pk=product_id)
    quantity = int(request.POST.get('quantity'))
    size = str(request.POST.get('size'))  # Convert size to string
    cart = request.session.get('cart', {})

    if str(product_id) in list(cart.keys()):
        if isinstance(cart[str(product_id)], dict) and 'items_by_size' in cart[str(product_id)]:
            if size in cart[str(product_id)]['items_by_size']:
                cart[str(product_id)]['items_by_size'][size] = quantity
                messages.success(request, f'Quantity of {product.name} size {size} in your cart has been updated!')
        else:
            cart[str(product_id)] = quantity
            messages.success(request, f'Quantity of {product.name} in your cart has been updated!')

    request.session['cart'] = cart
    request.session['cart_changed'] = True
    return redirect('cart_view')


def remove_from_cart(request, product_id):
    """
    Removes a specified product from the shopping cart. If the product has a size 
    option, the size is also taken into account.

    **Context**

    ``product_id``
    The ID of the product to be removed from the cart.

    ``cart``
    The current state of the shopping cart stored in the session.

    ``size``
    The size of the product, if applicable.

    **Methods**

    ``remove_from_cart(request, product_id)``
    Handles the logic for removing a product from the cart and updating the session 
    accordingly. Also manages success messages for user feedback.

    **Template:**

    :template:`redirect to the cart view`
    """
    product = get_object_or_404(Product, pk=product_id)
    size = request.POST.get('size')
    cart = request.session.get('cart', {})

    if str(product_id) in list(cart.keys()):
        if isinstance(cart[str(product_id)], dict) and 'items_by_size' in cart[str(product_id)]:
            if size in cart[str(product_id)]['items_by_size']:
                del cart[str(product_id)]['items_by_size'][size]
                messages.success(request, f'{product.name} size {size} has been removed from your cart!')
                # If there are no other sizes for this product, remove the product entry
                if not cart[str(product_id)]['items_by_size']:
                    del cart[str(product_id)]
        else:
            del cart[str(product_id)]
            messages.success(request, f'{product.name} has been removed from your cart!')

    request.session['cart'] = cart
    request.session['cart_changed'] = True
    return redirect('cart_view')