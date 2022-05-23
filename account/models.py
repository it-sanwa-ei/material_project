from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator
from django import forms

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.

class CustomUser(AbstractUser):
    username = models.CharField('username', max_length=25, null=False, blank=False, unique=True)
    email = models.EmailField(null=False, blank=False)
    
class UserAction(models.Model):
    sender = models.ForeignKey(CustomUser, related_name='user', on_delete=models.CASCADE)
    verb = models.CharField(max_length=255)
    target_ct = models.ForeignKey(ContentType, blank=True, null=True, related_name='target_obj', on_delete=models.CASCADE)
    target_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey('target_ct', 'target_id')
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ('-created',)

    def __str__(self):
        a = "{0.sender} | {0.verb}"
        return a.format(self)
