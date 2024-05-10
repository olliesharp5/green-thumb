from django.contrib import admin
from .models import Order, OrderLineItem


class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)

    readonly_fields = ('order_number', 'date',
                       'delivery_cost', 'order_total',
                       'grand_total','original_bag',
                       'stripe_pid')

    fields = ('order_number', 'date', 'full_name',
              'email', 'phone_number', 'country',
              'postcode', 'town_or_city', 'street_address1',
              'street_address2', 'county', 'delivery_cost',
              'order_total', 'grand_total', 'original_bag',
              'stripe_pid')

    list_display = ('order_number', 'date', 'full_name',
                    'order_total', 'delivery_cost',
                    'grand_total', 'view_line_items')

    ordering = ('-date',)
    
    search_fields = ['full_name', 'email', 'order_number']
    list_filter = ['date', 'delivery_cost', 'country']

    def view_line_items(self, obj):
        return "\n".join([str(line_item.product) for line_item in obj.lineitems.all()])

    view_line_items.short_description = 'Line Items'

admin.site.register(Order, OrderAdmin)