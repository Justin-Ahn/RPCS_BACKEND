from django.urls import path
from wt import views

urlpatterns = [
    path('patient', views.patient),
    path('caregiver', views.caregiver),
    path('safezone', views.safezone)
]