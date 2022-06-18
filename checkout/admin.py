from django.contrib import admin
from .models import Order, OrderLineItem


# Setting Admin view of OrderLineItem model's records in Django admin platform (under related Order)
class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


# Setting Admin view of Order model's records in Django admin platform
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


# Registering Order model (with related OrderLineItems) on Django admin platform
admin.site.register(Order, OrderAdmin)