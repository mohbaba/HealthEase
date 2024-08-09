from django.urls import path

from wallet import views

urlpatterns = [
    path('deposit', views.DepositViewSet.as_view()),
    path('paystack_callback', views.PaystackCallBackViewSet.as_view())
]
