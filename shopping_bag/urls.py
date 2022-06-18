from django.urls import path
from . import views

# Internal URLs of ShoppingBag application of Mind The Reader project
urlpatterns = [
    path('', views.view_my_bag, name='view_my_bag'),
    path('add/<item_id>/', views.add_to_my_bag, name='add_to_my_bag'),
    path('adjust/<item_id>/', views.adjust_my_bag, name='adjust_my_bag'),
    path('remove/<item_id>/', views.remove_from_my_bag, name='remove_from_my_bag'),
]