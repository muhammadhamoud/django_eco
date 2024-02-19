from django.urls import path, include
from .views import *

urlpatterns = [
    # path('vehicles/', VehicleListView.as_view(), name='vehicle_list'),
    # path('vehicle/<int:pk>/', VehicleDetailView.as_view(), name='vehicle_detail'),
    # path('vehicle/<int:vehicle_id>/reserve/', VehicleReservationView.as_view(), name='vehicle_reservation'),
]

