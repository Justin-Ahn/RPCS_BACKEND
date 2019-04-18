from django.urls import path
from ct import views

urlpatterns = [
    path('patient-incidents', views.patient_incidents),
    path('patient-trends', views.patient_trends)
]