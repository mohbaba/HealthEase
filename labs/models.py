from django.db import models

from users.models import UserProfile


# Create your models here.


class Lab(models.Model):
    name = models.CharField(max_length=100, default=None)
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='lab')
    location = models.CharField(max_length=255, blank=True, null=True)
    established_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Lab'
        verbose_name_plural = 'Labs'

    def __str__(self):
        return self.name
