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


class DepositSerializer(serializers.Serializer):
    wallet_id = serializers.CharField(max_length=10)
    amount = serializers.DecimalField(max_digits=15, decimal_places=2)


class WithdrawSerializer(serializers.Serializer):
    wallet_id = serializers.CharField(max_length=10)
    amount = serializers.DecimalField(max_digits=15, decimal_places=2)


class TransferSerializer(serializers.Serializer):
    sender = serializers.CharField(max_length=10)
    receiver = serializers.CharField(max_length=10)
    amount = serializers.DecimalField(max_digits=15, decimal_places=2)
