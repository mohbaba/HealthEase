from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import CASCADE

# from wallet.models import Wallet


# Create your models here.
ROLES = [
    ('PATIENT', 'PATIENT'),
    ('DOCTOR', 'DOCTOR'),
    ('PHARMACIST', 'PHARMACIST'),
    ('LABORATORY', 'LABORATORY'),
]


class UserProfile(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    phone_number = models.CharField(max_length=11, unique=True,validators = [
        RegexValidator(
            regex=r'^\d{11}$',
            message=_("Phone number must be exactly 11 digits."),
            code='invalid_phone_number'
        )
    ])
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')], default='Female')
    role = models.CharField(max_length=15, choices=ROLES, default='PATIENT')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']


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
