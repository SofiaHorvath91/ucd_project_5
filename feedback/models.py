from django.db import models
from django.contrib.auth import get_user_model
from ucd_project_5 import settings

User = get_user_model()


# Feedback object/model
# => Aim of object/model :
# Capture details of feedback provided by the user about the site (rating & comment)
# => Models/objects connected to Feedback model/object via ForeignKey relation :
# User (Owner)
class Feedback(models.Model):
    rating_point = models.IntegerField(null=True, blank=True)
    rating_description = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)


# Recommendation object/model
# => Aim of object/model :
# Capture details of item recommended by a standard user for the approval of admin user
# => Models/objects connected to Recommendation model/object via ForeignKey relation :
# User (Owner)
class Recommendation(models.Model):
    status = models.CharField(max_length=25, blank=True, null=True)
    title = models.CharField(max_length=254, null=True)
    author = models.CharField(max_length=254)
    category = models.CharField(max_length=254, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title

