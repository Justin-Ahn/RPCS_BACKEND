from django.urls import path
from ca import views

urlpatterns = [
    path('wandering', views.wandering),
    path('phys-measures', views.phys_measures),
    path('phys-incidents', views.phys_incidents),
    path('phys-model-params', views.phys_params),
    path('incident-summary', views.incident_summary)
    path('sleep_trends', views.sleep_trends),
]