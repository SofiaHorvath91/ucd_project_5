from django.contrib import admin
from .models import Order, OrderLineItem


class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)

    readonly_fields = ('order_number', 'date',
                       'delivery', 'order_total',
                       'grand_total', 'bag',
                       'stripe_pid')

    fields = ('order_number', 'profile', 'date', 'full_name',
              'email', 'phone', 'country',
              'postcode', 'city', 'street1',
              'street2', 'county', 'delivery',
              'order_total', 'grand_total', 'bag',
              'stripe_pid')

    list_display = ('order_number', 'date', 'full_name',
                    'order_total', 'delivery',
                    'grand_total',)

    ordering = ('-date',)


admin.site.register(Order, OrderAdmin)