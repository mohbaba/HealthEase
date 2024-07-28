from django.db import models
from users.models import UserProfile


# Create your models here.


class Pharmacy(models.Model):
    name = models.CharField(max_length=100, default=None)
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='pharmacy')

    class Meta:
        verbose_name = 'Pharmacy'
        verbose_name_plural = 'Pharmacies'

    def __str__(self):
        return self.name
