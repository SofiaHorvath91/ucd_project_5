from django.test import TestCase

from django.contrib.auth import get_user_model

User = get_user_model()


# Unit tests for User model
class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username="tester",
                                 email="test@test.com",
                                 is_staff=False)

    def test_user(self):
        user = User.objects.get(id=1)
        self.assertTrue(isinstance(user, User))
        self.assertEqual(user.username, "tester")
        self.assertEqual(user.email, "test@test.com")
        self.assertEqual(user.is_staff, False)