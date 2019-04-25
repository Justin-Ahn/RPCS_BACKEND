from django.urls import path
from int import views

urlpatterns = [
    path('patient-profile', views.patient_profile),
    path('caregiver-profile', views.caregiver_profile),
    path('doctor-profile', views.doctor_profile)
]
