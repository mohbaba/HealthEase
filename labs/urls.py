from django.urls import path
from .views import (
    LabListCreateView,
    LabRetrieveUpdateDestroyView,
    LabListFilterByName,
    LabListFilterByLocation,
    DeleteLab
)

urlpatterns = [
    path('labs/', LabListCreateView.as_view(), name='lab-list-create'),
    path('labs/<int:pk>/', LabRetrieveUpdateDestroyView.as_view(), name='lab-detail'),
    path('labs/filter/by_name/', LabListFilterByName.as_view(), name='lab-filter-by-name'),
    path('labs/filter/by_location/', LabListFilterByLocation.as_view(), name='lab-filter-by-location'),
    path('labs/delete/<int:pk>/', DeleteLab.as_view(), name='delete-lab'),
]