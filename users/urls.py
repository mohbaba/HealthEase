from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import  UserProfileViewSet, CustomTokenCreateView

router = DefaultRouter()
router.register('users', UserProfileViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('login/', CustomTokenCreateView.as_view(), name='login'),
]