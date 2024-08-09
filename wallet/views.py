from datetime import datetime
from decimal import Decimal

import requests
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from health_ease import settings
from .models import Wallet, Transaction
from .serializers import WalletSerializer, DepositSerializer
from .validators import validate_amount


class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer


class DepositViewSet(viewsets.ModelViewSet):

    def post(self, request):
        serializer = DepositSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        wallet_id = serializer.validated_data['wallet_id']
        amount = Decimal(serializer.validated_data['amount'])

        if amount <= 0:
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
            'callback_url': 'https://localhost:8000/wallet/paystack_callback',
            'metadata': {
                'wallet_id': wallet_id
            }
        }

        response = requests.post(paystack_url, json=data, headers=headers)
        response_data = response.json()

        if response.status_code != 200 or not response_data.get('status'):
            return Response({'error': 'Paystack transaction initialization failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        payment_url = response_data['data']['authorization_url']
        return Response({'payment_url': payment_url}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def withdraw(self, request, pk=None):
        wallet = self.get_object()
        amount = request.data.get('amount')
        description = request.data.get('description', 'Withdrawal')

        if not amount:
            return Response({'error': 'Amount is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Withdrawal amount must be positive")

            if wallet.amount < amount:
                raise ValueError("Insufficient funds")

            wallet.amount -= amount
            wallet.save()

            Transaction.objects.create(
                user=wallet.user,
                transaction_type='DEB',
                amount=amount,
                description=description
            )
            return Response({'status': 'Withdrawal successful'}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PaystackCallBackViewSet(viewsets.ModelViewSet):

    @csrf_exempt
    def paystack_callback(self, request):
        reference = request.GET.get('reference')

        if not reference:
            return JsonResponse({'error': 'No reference provided'}, status=400)

        paystack_url = f"https://api.paystack.co/transaction/verify/{reference}"
        headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
        }

        response = requests.get(paystack_url, headers=headers)
        response_data = response.json()

        if response.status_code != 200 or not response_data.get('status'):
            return JsonResponse({'error': 'Payment verification failed'}, status=400)

        payment_data = response_data['data']

        if payment_data['status'] == 'success':
            wallet = get_object_or_404(Wallet, pk=payment_data['metadata']['wallet_id'])
            amount = Decimal(payment_data['amount']) / 100
            wallet.amount += amount
            wallet.save()

            Transaction.objects.create(
                user=wallet.user,
                transaction_type='CRE',
                amount=amount,
                description="Deposit"
            )

            transaction_details = {
                'User': wallet.user.username,
                'amount': amount,
                'date': datetime.now(),
                'transaction_type': "CREDIT"
            }
            return JsonResponse(transaction_details, status=200)
        else:
            return JsonResponse({'error': 'Payment was not successful'}, status=400)
