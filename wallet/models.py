from datetime import datetime

from django.db import models
from django.db.models import DO_NOTHING, CASCADE
from django.utils import timezone

from users.models import UserProfile


# Create your models here.
class Transaction(models.Model):
    TRANSACTION_TYPE = [
        ('DEB', 'DEBIT'),
        ('CRE', 'CREDIT'),
        ('TRA', 'TRANSFER',),
    ]

    TRANSACTION_STATUS = [
        ('S', 'SUCCESSFUL'),
        ('F', 'FAIL'),
        ('P', 'PENDING',),
    ]
    user = models.ForeignKey(UserProfile, on_delete=DO_NOTHING)
    transaction_type = models.CharField(max_length=3, choices=TRANSACTION_TYPE, default='CRE')
    transaction_time = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.TextField()
    transaction_status = models.CharField(max_length=1, choices=TRANSACTION_STATUS, default='S')

    def __str__(self):
        return self.id


class Wallet(models.Model):
    amount = models.DecimalField(default=0, max_digits=15, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(UserProfile, on_delete=CASCADE)

    # transactions = models.ForeignKey(Transaction, on_delete=CASCADE)

    def _str_(self):
        return {self.id}
