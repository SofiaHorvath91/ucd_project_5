from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mindthereader.urls')),
    path('oauth/', include('social_django.urls', namespace='social')),
]

# Configure url path for static files (static/txt+img+css)
urlpatterns += staticfiles_urlpatterns()