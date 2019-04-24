from django.urls import path
from cg_doc import views

urlpatterns = [
    path('caregiver-profile', views.caregiver_profile),
    path('doctor-profile', views.doctor_profile)
]
