from django.urls import path
from hs import views

urlpatterns = [
    path('events', views.events),
    path('sensors', views.sensors)
]