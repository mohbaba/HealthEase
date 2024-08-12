from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import UserProfile
from wallet.models import Wallet


@receiver(signal=post_save, sender=UserProfile)
def create_account(created, instance, **kwargs):
    if created:
        Wallet.objects.create(
            user=instance,
        )
