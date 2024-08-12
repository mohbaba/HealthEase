from datetime import datetime
from decimal import Decimal

import requests
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from health_ease import settings
from .models import Wallet, Transaction
from .serializers import WalletSerializer, DepositSerializer, WithdrawSerializer, TransferSerializer
from .validators import validate_amount, validate_balance


class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer


class DepositView(APIView):
    serializer_class = DepositSerializer

    def post(self, request):
        serializer = DepositSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        wallet_id = serializer.validated_data['wallet_id']
        amount = Decimal(serializer.validated_data['amount'])

        if validate_amount(amount):
            return Response({'error': 'Deposit amount must be positive'}, status=status.HTTP_400_BAD_REQUEST)

        wallet = get_object_or_404(Wallet, pk=wallet_id)

        paystack_url = "https://api.paystack.co/transaction/initialize"
        headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
            'Content-Type': 'application/json',
        }
        data = {
            'email': wallet.user.email,
            'amount': int(amount * 100),
            'callback_url': 'http://127.0.0.1:8000/wallet/paystack_callback?reference=',
            'metadata': {
                'wallet_id': wallet_id
            }
        }

        response = requests.post(paystack_url, json=data, headers=headers)
        response_data = response.json()

        if response.status_code != 200 or not response_data.get('status'):
            return Response({'error': 'Paystack transaction initialization failed'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        authorization_url = response_data['data']['authorization_url']
        return redirect(authorization_url)


class PaystackCallbackView(APIView):

    @csrf_exempt
    def get(self, request):
        reference = request.GET.get('reference')

        if not reference:
            return JsonResponse({'error': 'No reference provided'}, status=400)

        paystack_url = f"https://api.paystack.co/transaction/verify/{reference}"
        headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
        }

        try:
            response = requests.get(paystack_url, headers=headers)
            response.raise_for_status()
            response_data = response.json()
        except requests.RequestException as e:
            return JsonResponse({'error': 'Payment verification request failed'}, status=500)

        payment_data = response_data.get('data', {})

        if not response_data.get('status') or payment_data.get('status') != 'success':
            return JsonResponse({'error': 'Payment verification failed or payment was not successful'}, status=400)

        wallet_id = payment_data.get('metadata', {}).get('wallet_id')
        wallet = get_object_or_404(Wallet, pk=wallet_id)
        amount = Decimal(payment_data['amount']) / 100
        wallet.amount += amount
        wallet.save()

        Transaction.objects.create(
            user=wallet.user,
            transaction_type='CRE',
            transaction_status='S',
            amount=amount,
            description="Deposit"
        )

        return JsonResponse({
            'User': wallet.user.username,
            'amount': amount,
            'date': datetime.now().isoformat(),
            'transaction_type': "CREDIT"
        }, status=200)


class WithdrawView(APIView):

    def post(self, request):
        serializer = WithdrawSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        wallet_id = serializer.validated_data['wallet_id']
        wallet = get_object_or_404(Wallet, pk=wallet_id)
        amount = Decimal(serializer.validated_data['amount'])

        if validate_amount(amount):
            return Response({'detail': 'Withdrawal amount must be positive'}, status=status.HTTP_400_BAD_REQUEST)

        if not validate_balance(wallet.amount, amount):
            return Response({'detail': 'Insufficient balance'}, status=status.HTTP_400_BAD_REQUEST)

        wallet.amount -= amount
        wallet.save()

        Transaction.objects.create(
            user=wallet.user,
            transaction_type='DEB',
            amount=amount,
            description='WITHDRAW'
        )
        return Response({'status': 'Withdraw successful'}, status=status.HTTP_200_OK)


class TransferView(APIView):
    def post(self, request):
        serializer = TransferSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sender = serializer.validated_data['sender']
        receiver = serializer.validated_data['receiver']
        amount = Decimal(serializer.validated_data['amount'])
