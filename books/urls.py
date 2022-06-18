from django.urls import path
from . import views

# Internal URLs of Books application of Mind The Reader project
urlpatterns = [
    path('', views.all_books, name='books'),
    path('<int:book_id>/', views.book_detail, name='book_detail'),
]

