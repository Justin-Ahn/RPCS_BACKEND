from django.urls import path
from watch import views

urlpatterns = [
    path('patient', views.patient),
    path('events', views.events),
]
