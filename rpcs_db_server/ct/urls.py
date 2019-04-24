from django.urls import path
from ct import views

urlpatterns = [
    path('patient-trends', views.patient_trends)
]