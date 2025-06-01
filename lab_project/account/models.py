from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager

# Create your models here.

class CustomUser(AbstractUser):
    mobile_no = models.CharField(max_length = 11, blank = True)
    email_verified = models.BooleanField(default = False)
    verf_link = models.CharField(max_length = 100)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    object = UserManager()