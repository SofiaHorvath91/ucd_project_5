from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_countries.fields import CountryField


# Profile object/model
# => Aim of object/model :
# Capture user delivery information
# => Models/objects connected to Profile model/object via OneToOne relation :
# User
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    basic_phone = models.CharField(max_length=20, null=True, blank=True)
    basic_street1 = models.CharField(max_length=80, null=True, blank=True)
    basic_street2 = models.CharField(max_length=80, null=True, blank=True)
    basic_city = models.CharField(max_length=40, null=True, blank=True)
    basic_county = models.CharField(max_length=80, null=True, blank=True)
    basic_postcode = models.CharField(max_length=20, null=True, blank=True)
    basic_country = CountryField(blank_label='Country', null=True, blank=True)

    def __str__(self):
        return self.user.username


# Create profile right upon user creation or save existing profile upon update
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    # Existing users: just save the profile
    instance.profile.save()