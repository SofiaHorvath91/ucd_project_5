import uuid

from django.db import models
from django.db.models import Sum
from django.conf import settings

from django_countries.fields import CountryField

from books.models import Book
from profiles.models import Profile


# Order object/model to represent an order the users can place
# => Aim of object/model :
# Capture details of an order consisted of books the user wishes to purchase
# => Models/objects connected to Order model/object via OneToOne relation :
# Profile model to represent the user who placed the order
# => Models/objects connected to Order model/object via OneToMany relation :
# OrderLineItem model to represent books with quantities which consist the order
class Order(models.Model):
    order_number = models.UUIDField(default=uuid.uuid4, null=False, editable=False)
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL,
                                null=True, blank=True, related_name='orders')
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(blank_label='Country *', null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    city = models.CharField(max_length=40, null=False, blank=False)
    street1 = models.CharField(max_length=80, null=False, blank=False)
    street2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    delivery = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    bag = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default='')

    # Generate random UUID order number
    def _generate_order_number(self):
        return uuid.uuid4().hex

    # Update order total based on unit price of added books and delivery fee (calculated based on total)
    def update_total(self):
        self.order_total = self.lineitems.aggregate(Sum('lineitem_total'))['lineitem_total__sum'] or 0
        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery = self.order_total * settings.STANDARD_DELIVERY_PERCENTAGE / 100
        else:
            self.delivery = 0
        self.grand_total = self.order_total + self.delivery
        self.save()

    # Generate and save random UUID order number if not already created
    def save_order_number(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super(Order, self).save(*args, **kwargs)


# OrderLineItem object/model to represent a book added to an order
# => Aim of object/model :
# Capture details of a book added to the present order with quantity & unit price for purchase
# => Models/objects connected to OrderLineItem model/object via OneToOne relation :
# Book model to represent the book which consists the order line item
# => Models/objects to which OrderLineItem is connected via OneToMany relation :
# Order model to collect and sum all present order line items
class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, null=False, blank=False, on_delete=models.CASCADE, related_name='lineitems')
    book = models.ForeignKey(Book, null=False, blank=False, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False)

    # Calculate current order line item's total price based on quantity * book's price
    def save(self, *args, **kwargs):
        self.lineitem_total = self.book.price * self.quantity
        super(OrderLineItem, self).save(*args, **kwargs)

    # Order line item's display : Related book's unique field + related order's unique field
    def __str__(self):
        return f'ISBN {self.book.isbn} on order {self.order.order_number}'
