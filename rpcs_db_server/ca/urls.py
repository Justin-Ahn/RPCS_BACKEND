from django.urls import path
from ca import views

urlpatterns = [
    path('wandering', views.wandering),
    path('phys-measures', views.phys_measures),
    path('phys-model-params', views.phys_params),
]