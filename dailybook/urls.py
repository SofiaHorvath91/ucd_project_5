from django.urls import path
from . import views

urlpatterns = [
    path('', views.quiz, name='quiz'),
    path('<int:result_id>/', views.result, name='result'),
]