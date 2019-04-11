from django.urls import path
from ga import views

urlpatterns = [
    path('logical', views.logical),
    path('semantic', views.semantic),
    path('procedural', views.procedural),
    path('episodic', views.episodic)
]