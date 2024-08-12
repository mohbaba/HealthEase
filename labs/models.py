from django.db import models
from users.models import UserProfile


class Lab(models.Model):
    name = models.CharField(max_length=100, default=None)
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='lab')
    location = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    contact_phone = models.CharField(max_length=20, blank=True, null=False)
    contact_email = models.EmailField(blank=True, null=True)
    opening_hours = models.CharField(max_length=100, blank=True, null=True)
    equipment_list = models.TextField(blank=True, null=True)
    capacity = models.PositiveIntegerField(blank=True, null=True)
    date_established = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = 'Lab'
        verbose_name_plural = 'Labs'

    def __str__(self):
        return self.name
