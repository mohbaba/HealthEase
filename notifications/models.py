from django.db import models
from django.utils import timezone

from users.models import UserProfile

# Create your models here.

NOTIFICATION_TYPES = [
    ('Prescription', 'Prescription'),
    ('Appointment', 'Appointment'),
    ('Vitals', 'Vitals'),
    ('Message', 'Message'),
    ('Reminder', 'Reminder'),
]


class Notification(models.Model):
    message = models.TextField()
    is_sent = models.BooleanField(default=False)

    recipient = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default=NOTIFICATION_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    related_id = models.IntegerField(null=True,
                                     blank=True)  # Can be used to store ID of related object (e.g., Prescription, Appointment)

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification for {self.recipient} - {self.notification_type}"
