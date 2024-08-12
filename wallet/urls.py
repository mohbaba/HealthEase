from django.urls import path
from .views import DepositView, PaystackCallbackView, WithdrawView

urlpatterns = [
    path('deposit/', DepositView.as_view()),
    path('paystack_callback/', PaystackCallbackView.as_view()),
    path('withdraw/', WithdrawView.as_view()),
]
