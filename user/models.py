from django.contrib.auth.models import AbstractUser
from django.db import models


class UserProfile(AbstractUser):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    image = models.ImageField(upload_to='profile-image', blank=True, null=True)
