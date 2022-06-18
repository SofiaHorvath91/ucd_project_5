from django.urls import path
from .views import(
    home,
    signin,
    signout,
    signup,
)

# Basic internal URLs of Mind The Reader project
urlpatterns = [
    path('', home, name="home"),
    path('signup/', signup, name='signup'),
    path('login/', signin, name='login'),
    path('logout/', signout, name='logout'),
]

# Configuration of custom 404 page
handler404 = 'mindthereader.views.entry_not_found'
