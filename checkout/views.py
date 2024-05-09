from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings

from products.models import Product
from cart.contexts import cart_contents
from .forms import OrderForm

import stripe

def checkout(request):

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

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

    current_cart = cart_contents(request)
    total = current_cart['grand_total']
    stripe_total = round(total * 100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
            Did you forget to set it in your environment?')

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'cart_items': cart_items,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)