from django.db import models
from users.models import UserProfile


# Create your models here.


class Pharmacy(models.Model):
    name = models.CharField(max_length=100, default='', blank=False, null=False)
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, blank=False, related_name='pharmacy')
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    opening_hours = models.TextField(blank=True, null=True)
    is_open_24_hours = models.BooleanField(default=False)
    website = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Pharmacy'
        verbose_name_plural = 'Pharmacies'

    def __str__(self):
        return self.name
