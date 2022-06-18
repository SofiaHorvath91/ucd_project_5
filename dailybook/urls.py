from django.urls import path
from . import views

# Internal URLs of DailyBook application of Mind The Reader project
urlpatterns = [
    path('', views.quiz, name='quiz'),
    path('<int:result_id>/', views.result, name='result'),
]