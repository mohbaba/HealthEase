from django.db import models

# Create your models here.

class Call(models.Model):
    timestamp = models.TimeField(auto_now_add=True)
    duration = models.FloatField(default=0)