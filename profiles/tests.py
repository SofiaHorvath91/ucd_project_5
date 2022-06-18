import re

from django.test import TestCase
from django_countries.fields import Country

from .models import Profile
from django.contrib.auth import get_user_model

User = get_user_model()


# Unit tests for Profile Model
class OrderModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username="tester",
                                        email="test@test.com",
                                        is_staff=False)
        profile = Profile.objects.filter(user=user).first()
        profile.basic_phone = '0123456789',
        profile.basic_country = 'UK',
        profile.basic_postcode = '0000',
        profile.basic_city = 'London',
        profile.basic_street1 = '221B',
        profile.basic_street2 = 'Baker Street',
        profile.basic_county = 'London',
        profile.save()

    def get_field_value(self, string):
        start = '('
        end = ','
        return string[string.find(start)+len(start):string.find(end)]

    def set_field_value(self, string):
        return "'" + string + "'"

    def test_fields_max_length(self):
        profile = Profile.objects.filter(id=1).first()
        max_length_phone = profile._meta.get_field('basic_phone').max_length
        max_length_postcode = profile._meta.get_field('basic_postcode').max_length
        max_length_city = profile._meta.get_field('basic_city').max_length
        max_length_street1 = profile._meta.get_field('basic_street1').max_length
        max_length_street2 = profile._meta.get_field('basic_street2').max_length
        max_length_county = profile._meta.get_field('basic_county').max_length
        self.assertEqual(max_length_phone, 20)
        self.assertLess(len(profile.basic_phone), max_length_phone)
        self.assertEqual(max_length_postcode, 20)
        self.assertLess(len(profile.basic_postcode), max_length_postcode)
        self.assertEqual(max_length_city, 40)
        self.assertLess(len(profile.basic_city), max_length_city)
        self.assertEqual(max_length_street1, 80)
        self.assertLess(len(profile.basic_street1), max_length_street1)
        self.assertEqual(max_length_street2, 80)
        self.assertLess(len(profile.basic_street2), max_length_street2)
        self.assertEqual(max_length_county, 80)
        self.assertLess(len(profile.basic_county), max_length_county)

    def test_fields_instances(self):
        profile = Profile.objects.filter(id=1).first()
        self.assertTrue(isinstance(profile.user, User))
        self.assertTrue(isinstance(profile.basic_phone, str))
        self.assertTrue(isinstance(profile.basic_postcode, str))
        self.assertTrue(isinstance(profile.basic_city, str))
        self.assertTrue(isinstance(profile.basic_street1, str))
        self.assertTrue(isinstance(profile.basic_street2, str))
        self.assertTrue(isinstance(profile.basic_county, str))
        self.assertTrue(isinstance(profile.basic_country, Country))

    def test_fields_values(self):
        profile = Profile.objects.filter(id=1).first()
        self.assertEqual(str(profile), profile.user.username)
        self.assertEqual(profile.user.username, 'tester')
        self.assertEqual(profile.user.email, 'test@test.com')
        self.assertEqual(profile.user.is_staff, False)
        self.assertFalse(profile.user.is_staff)
        self.assertEqual(self.get_field_value(profile.basic_country.code), self.set_field_value('UK'))
        self.assertEqual(self.get_field_value(profile.basic_phone), self.set_field_value('0123456789'))
        self.assertEqual(self.get_field_value(profile.basic_postcode), self.set_field_value('0000'))
        self.assertEqual(self.get_field_value(profile.basic_street1), self.set_field_value('221B'))
        self.assertEqual(self.get_field_value(profile.basic_street2), self.set_field_value('Baker Street'))
        self.assertEqual(self.get_field_value(profile.basic_county), self.set_field_value('London'))
        self.assertEqual(self.get_field_value(profile.basic_city), self.set_field_value('London'))
