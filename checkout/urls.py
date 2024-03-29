from django.urls import path
from . import views
from .webhooks import webhook

# Internal URLs of Checkout application of Mind The Reader project
urlpatterns = [
    path('', views.checking_out, name='checkout'),
    path('checkout_success/<order_number>', views.checkout_success, name='checkout_success'),
    path('cache_checkout_data/', views.cache_checkout_data, name='cache_checkout_data'),
    path('wh/', webhook, name='webhook'),
]