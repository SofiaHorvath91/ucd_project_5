from datetime import datetime

from django.test import TestCase

from .models import Feedback, Recommendation
from django.contrib.auth import get_user_model

User = get_user_model()


# Unit tests for Feedback model
class FeedbackModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        ratings = {
            1: "Terrible",
            2: "Not good",
            3: "Average",
            4: "Very good",
            5: "Amazing",
        }
        user = User.objects.create_user(username="tester",
                                        email="test@test.com")
        Feedback.objects.create(rating_point=min(ratings, key=lambda k: ratings[k][4]),
                                rating_description=ratings[4],
                                content="good",
                                created=datetime.now(),
                                user=user)

    def test_rating(self):
        feedback = Feedback.objects.get(id=1)
        self.assertTrue(isinstance(feedback.rating_point, int))
        self.assertEqual(feedback.rating_point, 4)
        self.assertEqual(feedback.rating_description, "Very good")

    def test_description(self):
        feedback = Feedback.objects.get(id=1)
        max_length = feedback._meta.get_field('rating_description').max_length
        self.assertTrue(isinstance(feedback.rating_description, str))
        self.assertEqual(max_length, 255)

    def test_content(self):
        feedback = Feedback.objects.get(id=1)
        max_length = feedback._meta.get_field('content').max_length
        self.assertTrue(isinstance(feedback.content, str))
        self.assertEqual(max_length, 355)

    def test_created_date(self):
        feedback = Feedback.objects.get(id=1)
        self.assertTrue(isinstance(feedback.created, datetime))

    def test_user(self):
        feedback = Feedback.objects.get(id=1)
        self.assertTrue(isinstance(feedback.user, User))
        self.assertEqual(feedback.user.username, "tester")
        self.assertEqual(feedback.user.email, "test@test.com")


# Unit tests for Recommendation model
class RecommendationModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username="tester",
                                        email="test@test.com")
        Recommendation.objects.create(status='Pending',
                                      title="Misery",
                                      author="Stephen King",
                                      category='SciFi-Fantasy-Horror',
                                      created=datetime.now(),
                                      user=user)

    def test_recommendation_name(self):
        recommendation = Recommendation.objects.get(id=1)
        recommendation_name = recommendation.author + " : " + recommendation.title
        self.assertEqual(str(recommendation), recommendation_name)

    def test_text_char_fields(self):
        recommendation = Recommendation.objects.get(id=1)
        max_length_status = recommendation._meta.get_field('status').max_length
        max_length_title = recommendation._meta.get_field('title').max_length
        max_length_author = recommendation._meta.get_field('author').max_length
        max_length_category = recommendation._meta.get_field('category').max_length
        self.assertEqual(recommendation.status, 'Pending')
        self.assertTrue(isinstance(recommendation.status, str))
        self.assertEqual(max_length_status, 25)
        self.assertLess(len(recommendation.status), max_length_status)
        self.assertEqual(recommendation.title, 'Misery')
        self.assertTrue(isinstance(recommendation.title, str))
        self.assertEqual(max_length_title, 254)
        self.assertLess(len(recommendation.title), max_length_title)
        self.assertEqual(recommendation.author, 'Stephen King')
        self.assertTrue(isinstance(recommendation.author, str))
        self.assertEqual(max_length_author, 254)
        self.assertLess(len(recommendation.author), max_length_author)
        self.assertEqual(recommendation.category, 'SciFi-Fantasy-Horror')
        self.assertTrue(isinstance(recommendation.category, str))
        self.assertEqual(max_length_category, 254)
        self.assertLess(len(recommendation.category), max_length_category)

    def test_created_date(self):
        recommendation = Recommendation.objects.get(id=1)
        self.assertTrue(isinstance(recommendation.created, datetime))

    def test_user(self):
        recommendation = Recommendation.objects.get(id=1)
        self.assertTrue(isinstance(recommendation.user, User))
        self.assertEqual(recommendation.user.username, "tester")
        self.assertEqual(recommendation.user.email, "test@test.com")
