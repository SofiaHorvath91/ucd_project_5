from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('', include('mindthereader.urls')),
    path('books/', include('books.urls')),
    path('shopping_bag/', include('shopping_bag.urls')),
]

# Configure url path for static files (static/txt+img+css)
urlpatterns += staticfiles_urlpatterns()