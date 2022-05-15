from django.urls import path
from .views import(
    home,
    signin,
    signout,
    signup,
)

urlpatterns = [
    path('', home, name="home"),
    path('signup/', signup, name='signup'),
    path('login/', signin, name='login'),
    path('logout/', signout, name='logout'),
]