from django.db import models

from users.models import UserProfile


# Create your models here.


class Lab(models.Model):
    name = models.CharField(max_length=100, default=None)
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='lab')


    class Meta:
        verbose_name = 'Lab'
        verbose_name_plural = 'Labs'

    def __str__(self):
        return self.name
