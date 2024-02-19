from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.properties_map, name="properties_map"),
    path('properties/', views.properties_geojson, name="properties_geojson"),
]