from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings

from products.models import Product
from cart.contexts import cart_contents
from profiles.models import UserProfile
from .forms import OrderForm
from .models import Order, OrderLineItem

import stripe
import json


@require_POST
def cache_checkout_data(request):
    """
    Caches checkout data in the payment intent's metadata before completing the payment process.

    **Context**

    ``pid``
    Payment Intent ID extracted from the client secret.

    ``cart``
    The current state of the shopping cart stored in the session.

    ``save_info``
    Whether to save the user's information for future purchases.

    ``username``
    The username of the logged-in user.

    **Methods**

    ``cache_checkout_data(request)``
    Modifies the Stripe Payment Intent with additional metadata. Handles errors by returning 
    an appropriate HTTP response and displaying an error message.

    **Returns**

    HTTP response with status 200 if successful, or 400 if an error occurs.
    """
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'cart': json.dumps(request.session.get('cart', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


def checkout(request):
    """
    Handles the checkout process, including rendering the checkout page and processing the order.

    **Context**

    ``stripe_public_key``
    The public key for Stripe payments.

    ``stripe_secret_key``
    The secret key for Stripe payments.

    ``intent``
    The payment intent created by Stripe.

    ``cart``
    The current state of the shopping cart stored in the session.

    ``order_form``
    An instance of `OrderForm` pre-filled with either the submitted data or the user's profile data.

    **Methods**

    ``checkout(request)``
    Handles both GET and POST requests. On POST, it processes the order form, creates the order 
    and order line items, and redirects to the checkout success page. On GET, it initializes the 
    payment intent and pre-fills the order form if the user is authenticated.

    **Template:**

    :template:`checkout/checkout.html`
    """
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    intent = None  # Ensure intent is initialized

    if request.method == 'POST':
        cart = request.session.get('cart', {})

        form_data = {
            'full_name': request.POST.get('full_name', ''),
            'email': request.POST.get('email', ''),
            'phone_number': request.POST.get('phone_number', ''),
            'country': request.POST.get('country', ''),
            'postcode': request.POST.get('postcode', ''),
            'town_or_city': request.POST.get('town_or_city', ''),
            'street_address1': request.POST.get('street_address1', ''),
            'street_address2': request.POST.get('street_address2', ''),
            'county': request.POST.get('county', ''),
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_cart = json.dumps(cart)
            # Add the user_profile to the order
            profile, created = UserProfile.objects.get_or_create(user=request.user)
            order.user_profile = profile
            order.save()
            for item_id, item_data in cart.items():
                try:
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        item_total = item_data * product.price
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data,
                            lineitem_total=item_total
                        )
                        order_line_item.save()
                    else:
                        for size, quantity in item_data['items_by_size'].items():
                            item_total = quantity * product.price
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=quantity,
                                product_size=size,
                                lineitem_total=item_total
                            )
                            order_line_item.save()
                except Product.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your cart wasn't found in our database. "
                        "Please call us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('cart_view'))

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(request, 'There was an error with your form. Please double check your information.')
    else:
        cart = request.session.get('cart', {})
        if not cart:
            messages.error(request, "There's nothing in your cart at the moment")
            return redirect(reverse('products'))

        current_cart = cart_contents(request)
        total = current_cart['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
            metadata={'cart': json.dumps(cart)},
        )
        
        if request.user.is_authenticated:
            # Get the user's profile
            user_profile = UserProfile.objects.get(user=request.user)
            # Create a dictionary with the user's saved information
            form_data = {
                'full_name': request.user.first_name + ' ' + request.user.last_name,
                'email': request.user.email,
                'phone_number': user_profile.default_phone_number,
                'country': user_profile.default_country,
                'postcode': user_profile.default_postcode,
                'town_or_city': user_profile.default_town_or_city,
                'street_address1': user_profile.default_street_address1,
                'street_address2': user_profile.default_street_address2,
                'county': user_profile.default_county,
            }
            # Create an instance of the form with the user's saved information
            order_form = OrderForm(initial=form_data)
        else:
            order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. Did you forget to set it in your environment?')

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret if intent else '',
    }

    return render(request, template, context)


def checkout_success(request, order_number, source=None):
    """
    Handles successful checkouts, including saving user information and clearing the cart.

    **Context**

    ``order_number``
    The order number of the successfully placed order.

    ``save_info``
    A flag indicating whether to save the user's information for future purchases.

    ``profile``
    The user's profile to update with the order's contact information.

    **Methods**

    ``checkout_success(request, order_number, source=None)``
    Retrieves the order using the order number, updates the user's profile if `save_info` is set,
    and clears the cart from the session. Displays a success message to the user.

    **Template:**

    :template:`checkout/checkout_success.html`
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)

    if save_info:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        profile.default_phone_number = order.phone_number
        profile.default_street_address1 = order.street_address1
        profile.default_street_address2 = order.street_address2
        profile.default_town_or_city = order.town_or_city
        profile.default_county = order.county
        profile.default_postcode = order.postcode
        profile.default_country = order.country
        profile.save()

    if source != 'profile':
        messages.success(request, f'Order successfully processed! \
            Your order number is {order_number}. A confirmation \
            email will be sent to {order.email}.')

    if 'cart' in request.session:
        del request.session['cart']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
