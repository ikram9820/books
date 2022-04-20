from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    bio = models.TextField(null=True,blank=True,)
    email= models.EmailField(unique=True)
    def __str__(self) -> str:
        return self.username





