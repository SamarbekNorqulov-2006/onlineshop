
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=13, unique=True, null=True, blank=True)
    auth_type = models.CharField(max_length=20, default='email')
    auth_status = models.CharField(max_length=20, default='new')
