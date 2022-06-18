from django.urls import path
from . import views

# Internal URLs of Feedback application of Mind The Reader project
urlpatterns = [
    path('', views.feedback, name='feedback'),
    path('subscribe/', views.subscribe, name='subscribe'),
]