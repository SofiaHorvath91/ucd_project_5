from datetime import datetime
from decimal import Decimal
from uuid import UUID

from django_countries.fields import Country

from django.conf import settings
from django.db.models import Sum
from django.test import TestCase

from .models import Order, OrderLineItem
from books.models import Book, Category
from profiles.models import Profile
from django.contrib.auth import get_user_model

User = get_user_model()


# Unit tests for Order Model
class OrderModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='SciFi-Fantasy-Horror',
                                friendly_name='SciFi-Fantasy-Horror')

        Book.objects.create(name='A Game of Thrones',
                            author='George R. R. Martin',
                            format='Paperback',
                            book_depository_stars=4.50,
                            price=10.77,
                            isbn='9780553573404',
                            category=Category.objects.get(id=1))

        user = User.objects.create_user(username="tester", email="test@test.com")
        profile = Profile.objects.filter(user=user).first()

        Order.objects.create(
            order_number=UUID('a4330828-4728-4375-b6ea-b04a4402377e'),
            profile=profile,
            full_name='Test User',
            email='test@test.com',
            phone='0123456789',
            country='UK',
            postcode='0000',
            city='London',
            street1='221B',
            street2='Baker Street',
            county='London',
            date=datetime.now(),
            delivery=1.08,
            order_total=10.77,
            grand_total=11.85,
            bag='{"3706": 1}',
            stripe_pid='pi_3L9HZnL4hisNfE1i0eYW3xsh'
        )

        OrderLineItem.objects.create(
            order=Order.objects.get(id=1),
            book=Book.objects.get(id=1),
            quantity=1,
            lineitem_total=10.77
        )

    def test_fields_max_length(self):
        order = Order.objects.get(id=1)
        max_length_full_name = order._meta.get_field('full_name').max_length
        max_length_email = order._meta.get_field('email').max_length
        max_length_phone = order._meta.get_field('phone').max_length
        max_length_postcode = order._meta.get_field('postcode').max_length
        max_length_city = order._meta.get_field('city').max_length
        max_length_street1 = order._meta.get_field('street1').max_length
        max_length_street2 = order._meta.get_field('street2').max_length
        max_length_county = order._meta.get_field('county').max_length
        max_length_stripe_pid = order._meta.get_field('stripe_pid').max_length
        self.assertEqual(max_length_full_name, 50)
        self.assertEqual(max_length_email, 254)
        self.assertEqual(max_length_phone, 20)
        self.assertEqual(max_length_postcode, 20)
        self.assertEqual(max_length_city, 40)
        self.assertEqual(max_length_street1, 80)
        self.assertEqual(max_length_street2, 80)
        self.assertEqual(max_length_county, 80)
        self.assertEqual(max_length_stripe_pid, 254)

    def test_fields_max_digits_decimals(self):
        order = Order.objects.get(id=1)
        max_digits_delivery = order._meta.get_field('delivery').max_digits
        decimal_places_delivery = order._meta.get_field('delivery').decimal_places
        max_digits_order_total = order._meta.get_field('order_total').max_digits
        decimal_places_order_total = order._meta.get_field('order_total').decimal_places
        max_digits_grand_total = order._meta.get_field('grand_total').max_digits
        decimal_places_grand_total = order._meta.get_field('grand_total').decimal_places
        self.assertEqual(max_digits_delivery, 6)
        self.assertEqual(decimal_places_delivery, 2)
        self.assertEqual(max_digits_order_total, 10)
        self.assertEqual(decimal_places_order_total, 2)
        self.assertEqual(max_digits_grand_total, 10)
        self.assertEqual(decimal_places_grand_total, 2)

    def test_order_number(self):
        order = Order.objects.get(id=1)
        editable_order_number = order._meta.get_field('order_number').editable
        self.assertTrue(isinstance(order.order_number, UUID))
        self.assertEqual(editable_order_number, False)

    def test_order_total(self):
        order = Order.objects.get(id=1)
        order_total = order.lineitems.aggregate(Sum('lineitem_total'))['lineitem_total__sum']
        default_order_total = order._meta.get_field('order_total').default
        self.assertEqual(order.order_total, order_total)
        self.assertEqual(default_order_total, 0)
        self.assertTrue(isinstance(order.order_total, Decimal))

    def test_delivery(self):
        order = Order.objects.get(id=1)
        delivery = round(order.order_total * settings.STANDARD_DELIVERY_PERCENTAGE / 100, 2)
        default_delivery = order._meta.get_field('delivery').default
        self.assertEqual(order.delivery, delivery)
        self.assertEqual(default_delivery, 0)
        self.assertTrue(isinstance(order.delivery, Decimal))

    def test_grand_total(self):
        order = Order.objects.get(id=1)
        grand_total = order.order_total + order.delivery
        default_grand_total = order._meta.get_field('grand_total').default
        self.assertEqual(order.grand_total, grand_total)
        self.assertEqual(default_grand_total, 0)
        self.assertTrue(isinstance(order.grand_total, Decimal))

    def test_format_phone_email(self):
        order = Order.objects.get(id=1)
        phone_regex = r"^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$"
        email_regex = r"\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b"
        self.assertRegex(order.phone, phone_regex)
        self.assertRegex(order.email, email_regex)

    def test_fields_instances(self):
        order = Order.objects.get(id=1)
        self.assertTrue(isinstance(order.profile, Profile))
        self.assertTrue(isinstance(order.lineitems.first(), OrderLineItem))
        self.assertTrue(isinstance(order.full_name, str))
        self.assertTrue(isinstance(order.country, Country))
        self.assertEqual(order.country, Country(code='UK'))
        self.assertTrue(isinstance(order.county, str))
        self.assertTrue(isinstance(order.postcode, str))
        self.assertTrue(isinstance(order.city, str))
        self.assertTrue(isinstance(order.street1, str))
        self.assertTrue(isinstance(order.street2, str))
        self.assertTrue(isinstance(order.stripe_pid, str))
        self.assertTrue(isinstance(order.bag, str))
        self.assertEqual(order._meta.get_field('bag').default, '')
        self.assertTrue(isinstance(order.date, datetime))
        self.assertTrue(isinstance(order.delivery, Decimal))
        self.assertTrue(isinstance(order.order_total, Decimal))
        self.assertTrue(isinstance(order.grand_total, Decimal))


# Unit tests for OrderLineItem Model
class OrderLineModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='SciFi-Fantasy-Horror',
                                friendly_name='SciFi-Fantasy-Horror')

        Book.objects.create(name='A Game of Thrones',
                            author='George R. R. Martin',
                            format='Paperback',
                            book_depository_stars=4.50,
                            price=10.77,
                            isbn='9780553573404',
                            category=Category.objects.get(id=1))

        user = User.objects.create_user(username="tester", email="test@test.com")
        profile = Profile.objects.filter(user=user).first()

        Order.objects.create(
            order_number=UUID('a4330828-4728-4375-b6ea-b04a4402377e'),
            profile=profile,
            full_name='Test User',
            email='test@test.com',
            phone='0123456789',
            country='UK',
            postcode='0000',
            city='London',
            street1='221B',
            street2='Baker Street',
            county='London',
            date=datetime.now(),
            delivery=2.15,
            order_total=21.54,
            grand_total=23.69,
            bag='{"3706": 1}',
            stripe_pid='pi_3L9HZnL4hisNfE1i0eYW3xsh'
        )

        OrderLineItem.objects.create(
            order=Order.objects.get(id=1),
            book=Book.objects.get(id=1),
            quantity=2,
            lineitem_total=21.54
        )

    def name_lineitem(self):
        orderlineitem = Order.objects.get(id=1).lineitems.first()
        self.assertEqual(str(orderlineitem),
                         'ISBN 9780553573404 on order a4330828-4728-4375-b6ea-b04a4402377e')

    def test_lineitem_total(self):
        order = Order.objects.get(id=1)
        orderlineitem = order.lineitems.first()
        lineitem_total = orderlineitem.book.price * orderlineitem.quantity
        lineitem_unitprice = orderlineitem.lineitem_total / orderlineitem.quantity
        delivery_orderlineitems = round(orderlineitem.lineitem_total * settings.STANDARD_DELIVERY_PERCENTAGE/100, 2)
        editable_lineitem_total = orderlineitem._meta.get_field('lineitem_total').editable
        max_digits_lineitem_total = orderlineitem._meta.get_field('lineitem_total').max_digits
        decimal_places_lineitem_total = orderlineitem._meta.get_field('lineitem_total').decimal_places
        self.assertEqual(max_digits_lineitem_total, 6)
        self.assertEqual(decimal_places_lineitem_total, 2)
        self.assertEqual(orderlineitem.lineitem_total, lineitem_total)
        self.assertEqual(lineitem_unitprice, orderlineitem.book.price)
        self.assertEqual(delivery_orderlineitems, order.delivery)
        self.assertEqual(editable_lineitem_total, False)
        self.assertTrue(isinstance(order.grand_total, Decimal))

    def test_fields_instances(self):
        orderlineitem = Order.objects.get(id=1).lineitems.first()
        self.assertTrue(isinstance(orderlineitem.order, Order))
        self.assertTrue(isinstance(orderlineitem.book, Book))
        self.assertTrue(isinstance(orderlineitem.lineitem_total, Decimal))
        self.assertTrue(isinstance(orderlineitem.quantity, int))
        self.assertEqual(orderlineitem._meta.get_field('quantity').default, 0)
