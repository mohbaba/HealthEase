from django.urls import path

from users.views import UserRegistration

urlpatterns = [
    path('registerUser', UserRegistration.as_view(), name='register-user')
]