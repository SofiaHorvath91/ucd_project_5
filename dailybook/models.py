from django.db import models
from django.contrib.auth import get_user_model
from ucd_project_5 import settings
from books.models import Book, Category

User = get_user_model()


# Quiz object/model to represent a quiz with questions/answers
# => Aim of object/model :
# Capture details of a quiz which has questions
# with related answers and results upon completion
# => Models/objects connected to Quiz model/object via OneToMany relation :
# Question to represent a question posed during the quiz
# Result to represent the user result upon quiz completion
class Quiz(models.Model):
    name = models.CharField(max_length=254)
    description = models.TextField(max_length=354, blank=True, null=True)


# Question object/model to represent a question the user should answer
# => Aim of object/model :
# Capture details of question
# to be answered while completing the quiz
# => Models/objects connected to Question model/object via OneToMany relation :
# Answer to represent a selectable answer to the given question
# => Models/objects to which Question model/object is connected via OneToMany relation :
# Quiz to represent a selectable answer to the given question
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, null=False, blank=False, on_delete=models.CASCADE, related_name='questions')
    number = models.IntegerField(blank=True, null=True)
    question = models.TextField(max_length=254, blank=True, null=True)


# Answer object/model to represent an answer the user can select for a question
# => Aim of object/model :
# Capture details of an answer which can be
# chosen by the user for a given question
# => Models/objects connected to Answer model/object via OneToOne relation :
# Category to represent the book genre connected
# to the answer (hidden from user, for backend use for result)
# => Models/objects to which Answer model/object is connected via OneToMany relation :
# Question to represent the question for which the answer can be selected
class Answer(models.Model):
    answer = models.TextField(max_length=254, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    question = models.ForeignKey(Question, null=False, blank=False, on_delete=models.CASCADE, related_name='answers')


# Result object/model to represent a result after answering all quiz questions
# => Aim of object/model :
# Capture details of the result which is
# calculated for the user upon quiz completion, based on answers
# => Models/objects connected to Result model/object via OneToOne relation :
# - Category to represent the book genre
#   which was chosen the most often (via choosing answer)
# - Book to represent the recommended book
#   in the genre represented by Category
# - User to represent the user
#   who filled out the quiz and got the result
# => Models/objects to which Result model/object is connected via OneToMany relation :
# Quiz to represent the quiz which was completed to get this result
class Result(models.Model):
    quiz = models.ForeignKey(Quiz, null=False, blank=False, on_delete=models.CASCADE, related_name='results')
    point = models.IntegerField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    result = models.TextField(max_length=354, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
