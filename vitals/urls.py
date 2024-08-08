from django.urls import path
from django.urls import include
from rest_framework.routers import DefaultRouter

from vitals.views import BloodPressureCreateView, BloodPressureRetrieveUpdateDestroyView, BloodSugarViewSet, \
    HeartRateViewSet, BMIViewSet, TemperatureViewSet, WeightViewSet, HeightViewSet, VitalsViewSet

router = DefaultRouter()
router.register(r'blood-sugar', BloodSugarViewSet)
router.register(r'heart-rate', HeartRateViewSet)
router.register(r'bmi', BMIViewSet)
router.register(r'temperature', TemperatureViewSet)
router.register(r'weight', WeightViewSet)
router.register(r'height', HeightViewSet)
router.register(r'vitals', VitalsViewSet)

urlpatterns = [
    path('addVitals', BloodPressureCreateView.as_view(), name='add_blood_pressure'),
    path('bloodPressure/<int:pk>', BloodPressureRetrieveUpdateDestroyView.as_view(), name='blood_pressure'),
    path('', include(router.urls))
]