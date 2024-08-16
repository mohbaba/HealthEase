from django.urls import path, include
from rest_framework.routers import DefaultRouter

from appointment.views import AppointmentViewSet

router = DefaultRouter()
router.register(r'appointment', AppointmentViewSet, basename='appointment')

urlpatterns = [
    path('', include(router.urls))
]