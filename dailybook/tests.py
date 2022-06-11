from datetime import datetime

from django.test import TestCase

from .models import Quiz, Question, Answer, Result
from books.models import Book, Category
from django.contrib.auth import get_user_model

User = get_user_model()

# Testing Quiz / Question / Answer / Result Models
class QuizQuestionAnswerResultModelsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='SciFi-Fantasy-Horror',
                                friendly_name='SciFi-Fantasy-Horror')

        Category.objects.create(name='Crime-Thriller',
                                friendly_name='Crime-Thriller')

        Book.objects.create(name='A Game of Thrones',
                            author='George R. R. Martin',
                            format='Paperback',
                            book_depository_stars=4.50,
                            price=10.77,
                            isbn='9780553573404',
                            category=Category.objects.get(name='SciFi-Fantasy-Horror'))

        Quiz.objects.create(name='Test Quiz',
                            description='Sample quiz for testing')

        Question.objects.create(quiz=Quiz.objects.get(id=1),
                                number=1,
                                question="First Question?")

        Answer.objects.create(question=Question.objects.get(id=1),
                              category=Category.objects.get(name='SciFi-Fantasy-Horror'),
                              answer="Answer1")

        Answer.objects.create(question=Question.objects.get(id=1),
                              category=Category.objects.get(name='Crime-Thriller'),
                              answer="Answer2")

        user = User.objects.create_user(username="tester", email="test@test.com")

        Result.objects.create(quiz=Quiz.objects.get(name='Test Quiz'),
                              point=1,
                              category=Answer.objects.get(id=1).category,
                              book=Book.objects.get(id=1),
                              user=user,
                              result="Daily mood is for SciFi-Fantasy-Horror",
                              created=datetime.now())

    def test_models_fields_max_length(self):
        quiz = Quiz.objects.get(id=1)
        question = quiz.questions.first()
        answer = question.answers.first()
        result = quiz.results.first()
        max_length_quiz_name = quiz._meta.get_field('name').max_length
        max_length_quiz_description = quiz._meta.get_field('description').max_length
        max_length_question_question = question._meta.get_field('question').max_length
        max_length_answer_answer = answer._meta.get_field('answer').max_length
        max_length_result_result = result._meta.get_field('result').max_length
        self.assertEqual(max_length_quiz_name, 254)
        self.assertEqual(max_length_quiz_description, 354)
        self.assertEqual(max_length_question_question, 254)
        self.assertEqual(max_length_answer_answer, 254)
        self.assertEqual(max_length_result_result, 354)

    def test_models_fields_instances(self):
        quiz = Quiz.objects.get(id=1)
        question = quiz.questions.first()
        answer = question.answers.first()
        result = quiz.results.first()
        self.assertTrue(isinstance(quiz.name, str))
        self.assertTrue(isinstance(quiz.description, str))
        self.assertTrue(isinstance(question.quiz, Quiz))
        self.assertTrue(isinstance(question.number, int))
        self.assertTrue(isinstance(question.question, str))
        self.assertTrue(isinstance(answer.question, Question))
        self.assertTrue(isinstance(answer.category, Category))
        self.assertTrue(isinstance(answer.answer, str))
        self.assertTrue(isinstance(result.quiz, Quiz))
        self.assertTrue(isinstance(result.category, Category))
        self.assertTrue(isinstance(result.book, Book))
        self.assertTrue(isinstance(result.user, User))
        self.assertTrue(isinstance(result.point, int))
        self.assertTrue(isinstance(result.result, str))
        self.assertTrue(isinstance(result.created, datetime))

    def test_models_relations(self):
        quiz = Quiz.objects.get(id=1)
        questions_count = len(quiz.questions.all())
        answers_count = len(quiz.questions.first().answers.all())
        results_count = len(quiz.results.all())
        result_category_count = len(Result.objects.filter(category__name='SciFi-Fantasy-Horror').all())
        result_answer_count = len(Answer.objects.filter(category=quiz.results.first().category).all())
        result_book_count = len(Book.objects.filter(id=quiz.results.first().book.id).all())
        result_user_count = len(User.objects.filter(id=quiz.results.first().user.id).all())
        self.assertEqual(questions_count, 1)
        self.assertEqual(answers_count, 2)
        self.assertEqual(results_count, 1)
        self.assertEqual(result_category_count, 1)
        self.assertEqual(result_answer_count, 1)
        self.assertEqual(result_book_count, 1)
        self.assertEqual(result_user_count, 1)



