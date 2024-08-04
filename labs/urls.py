from django.urls import path
from .views import LabListCreateView, LabRetrieveUpdateDestroyView

urlpatterns = [
    path('labs/', LabListCreateView.as_view(), name='lab-list-create'),
    path('labs/<int:pk>/', LabRetrieveUpdateDestroyView.as_view(), name='lab-detail'),
]