from django.contrib.auth import get_user_model

# Referencing the standard Django User model
# => Aim of object/model :
# Capture details of connected user for login/signup function
User = get_user_model()
