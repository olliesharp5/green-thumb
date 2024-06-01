from django.shortcuts import get_object_or_404
from django.conf import settings
from decimal import Decimal

from products.models import Product

def cart_contents(request):
    """
    Retrieve the contents of the shopping cart from the session and calculate the total cost, delivery charges,
    and other relevant details.

    Args:
        request: HttpRequest object containing session data with the cart information.

    Returns:
        dict: A dictionary containing the following keys:
            - cart_items (list): A list of dictionaries, each containing details of a product in the cart such as:
                - product_id (int): The ID of the product.
                - quantity (int): The quantity of the product.
                - product (Product): The Product object.
                - total (Decimal): The total price for this product based on the quantity.
                - size (str, optional): The size of the product, if applicable.
            - total (Decimal): The total cost of all products in the cart.
            - product_count (int): The total number of products in the cart.
            - delivery (Decimal): The delivery charge based on the cart total and delivery settings.
            - free_delivery_delta (Decimal): The remaining amount required to qualify for free delivery.
            - free_delivery_threshold (Decimal): The minimum amount required to qualify for free delivery.
            - grand_total (Decimal): The grand total cost including delivery charges.
            - cart_changed (bool): A flag indicating if the cart has changed.

    Raises:
        Http404: If any of the products in the cart cannot be found in the database.
    """
    
    cart = request.session.get('cart', {})
    cart_changed = request.session.get('cart_changed', False)

    cart_items = []
    total = 0
    product_count = 0

    for product_id, item_data in cart.items():
        product = get_object_or_404(Product, pk=product_id)
        if isinstance(item_data, int):
            item_total = item_data * product.price
            total += item_total
            product_count += item_data
            cart_items.append({
                'product_id': product_id,
                'quantity': item_data,
                'product': product,
                'total': item_total,
            })
        else:
            for size, quantity in item_data['items_by_size'].items():
                item_total = quantity * product.price
                total += item_total
                product_count += quantity
                cart_items.append({
                    'product_id': product_id,
                    'quantity': quantity,
                    'product': product,
                    'total': item_total,
                    'size': size,
                })

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = delivery + total

    context = {
        'cart_items': cart_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
        'cart_changed': cart_changed, 
    }

    return context