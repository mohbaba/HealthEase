from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CASCADE


# from wallet.models import Wallet


# Create your models here.


class UserProfile(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    phone_number = models.CharField(max_length=11, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'username']

    def __str__(self):
        return self.email


class Address(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=CASCADE)
    house_number = models.IntegerField()
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.house_number}, {self.street}, {self.city}, {self.state}"
