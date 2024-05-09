from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import OrderForm
from products.models import Product

def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "There's nothing in your cart at the moment")
        return redirect(reverse('products'))

    cart_items = []
    for item_id, item_data in cart.items():
        product = Product.objects.get(id=item_id)
        if isinstance(item_data, dict):
            for size, quantity in item_data['items_by_size'].items():
                subtotal = product.price * quantity
                cart_items.append({
                    'product_id': item_id,
                    'quantity': quantity,
                    'product': product,
                    'subtotal': subtotal,
                    'size': size,
                })
        else:
            quantity = item_data
            subtotal = product.price * quantity
            cart_items.append({
                'product_id': item_id,
                'quantity': quantity,
                'product': product,
                'subtotal': subtotal,
            })


    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'cart_items': cart_items,
    }

    return render(request, template, context)