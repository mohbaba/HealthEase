from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import UserRegistration, UserProfileViewSet

router = DefaultRouter()
router.register('users', UserProfileViewSet)
urlpatterns = [
    # path('registerUser', UserRegistration.as_view(), name='register-user'),
    path('', include(router.urls)),
]