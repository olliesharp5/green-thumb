from django.shortcuts import get_object_or_404
from decimal import Decimal
from django.conf import settings
from products.models import Product

def cart_contents(request):
    cart = request.session.get('cart', {})

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
    }

    return context