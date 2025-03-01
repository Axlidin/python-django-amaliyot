from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    profile_pic = models.ImageField(default='default_profile_pic.png')

    def __str__(self):
        return self.username