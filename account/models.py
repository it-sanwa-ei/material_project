from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator
from django import forms

# Create your models here.

class CustomUser(AbstractUser):
    username = models.CharField('username', max_length=25, null=False, blank=False, unique=True)
    email = models.EmailField(null=False, blank=False)