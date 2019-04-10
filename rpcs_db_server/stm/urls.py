from django.urls import path
from stm import views

urlpatterns = [
    path('tests', views.tests),
]
