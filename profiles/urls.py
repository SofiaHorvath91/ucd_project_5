from django.urls import path
from . import views

# Internal URLs of Profiles application of Mind The Reader project
urlpatterns = [
    path('', views.profile, name='profile'),
    path('order_history/<order_number>', views.order_history, name='order_history'),
]