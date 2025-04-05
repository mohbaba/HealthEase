from django.urls import path, include
from rest_framework.routers import DefaultRouter

from appointment.views import AppointmentViewSet, GetAppointment

router = DefaultRouter()
router.register(r'appointment', AppointmentViewSet, basename='appointment')

urlpatterns = [
    path('', include(router.urls)),
    path('getAppointment/', GetAppointment.as_view(), name='get-appointment')
]