from django.db import models
from django.contrib.auth import get_user_model
from ucd_project_5 import settings
from books.models import Book, Category

User = get_user_model()


class Quiz(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, null=False, blank=False, on_delete=models.CASCADE, related_name='questions')
    number = models.IntegerField(blank=True, null=True)
    question = models.TextField(blank=True, null=True)


class Answer(models.Model):
    answer = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    question = models.ForeignKey(Question, null=False, blank=False, on_delete=models.CASCADE, related_name='answers')


class Result(models.Model):
    quiz = models.ForeignKey(Quiz, null=False, blank=False, on_delete=models.CASCADE, related_name='results')
    point = models.IntegerField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    result = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)