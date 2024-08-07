from rest_framework import serializers
from .models import Transaction, Wallet


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'user', 'transaction_type', 'transaction_time', 'amount', 'description', 'transaction_status']
        read_only_fields = ['id', 'transaction_time']


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id', 'amount', 'date', 'status', 'user']
        read_only_fields = ['id', 'date']
