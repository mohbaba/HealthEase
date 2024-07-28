from django.db import models

# Create your models here.

class Notification(models.Model):
    message = models.TextField()
    recipient_id = models.IntegerField()
    is_sent = models.BooleanField(default=False)