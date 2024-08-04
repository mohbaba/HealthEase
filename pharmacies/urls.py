from django.urls import path
from . import views


urlpatterns = [
    path('register_pharmacy/', views.RegisterPharmacyView.as_view(), name='register_pharmacy'),
    path('update_pharmacy/<int:pk>/', views.UpdatePharmacyView.as_view(), name='update_pharmacy'),
    path('delete_pharmacy/<int:pk>/', views.DeletePharmacyView.as_view(), name='delete_pharmacy'),
    path('pharmacies/', views.ListPharmacyView.as_view(), name='list_pharmacies'),
    path('pharmacies/<int:pk>/', views.RetrievePharmacyView.as_view(), name='retrieve_pharmacy'),
    path('pharmacies/filter/', views.FilterListPharmacyView.as_view(), name='filter_pharmacies'),
]