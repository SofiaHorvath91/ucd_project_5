from django import template


register = template.Library()


# Tool to calculate subtotal for bag line items
@register.filter(name='calc_subtotal')
def calc_subtotal(price, quantity):
    return price * quantity