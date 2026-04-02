from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    
    # Using CharField for the name. 
    # By default, blank=False and null=False, making it mandatory.
    name = models.CharField(max_length=100, unique=True)

    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)

    USERNAME_FIELD = 'email'
    
    # Since 'name' is now mandatory, you must add it to REQUIRED_FIELDS 
    # so Django prompts for it when you create a superuser.
    REQUIRED_FIELDS = ['username', 'name']

    def __str__(self):
        return self.email
