from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import  UserProfileViewSet, CustomTokenCreateView, get_user_by_uid, get_user_by_email

router = DefaultRouter()
router.register('users', UserProfileViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('login/', CustomTokenCreateView.as_view(), name='login'),
    path('user_uid/', get_user_by_uid, name='get_user_by_uid'),
    path('user_email/<str:email>', get_user_by_email, name='get_user_by_email'),
]