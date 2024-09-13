from django.urls import path

from doctors.views import DoctorCreate, PrescribeMedicineView, MedicineView, MedicineRetrieveUpdateDestroy, \
    PrescriptionRetrieveDestroyView, DoctorRetrieveUpdateDestroyView, DoctorsNoteCreate, DoctorsNoteRetrieveUpdateDeleteView

urlpatterns = [
    path('auth/registerDoctor/', DoctorCreate.as_view(), name='register_doctor'),
    path('doctors/', DoctorCreate.as_view(), name='doctor_list'),
    path('prescribeMedicine', PrescribeMedicineView.as_view(), name='prescribe'),
    path('addDrug', MedicineView.as_view(), name='add-drug'),
    path('doctors/<int:pk>', DoctorRetrieveUpdateDestroyView.as_view(), name='update-doctor'),
    path('medicine/<int:pk>', MedicineRetrieveUpdateDestroy.as_view(), name='medicine'),
    path('prescription/<int:pk>', PrescriptionRetrieveDestroyView.as_view(), name='prescription'),
    path('doctorsNote/create', DoctorsNoteCreate.as_view(), name='doctors_note'),
    path('doctorsNote/<int:pk>', DoctorsNoteRetrieveUpdateDeleteView.as_view(), name='doctors_note-detail'),
]
