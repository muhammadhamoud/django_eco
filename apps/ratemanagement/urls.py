from django.urls import path, include
from .views import *

urlpatterns = [
    # path('vehicles/', VehicleListView.as_view(), name='vehicle_list'),
    # path('vehicle/<int:pk>/', VehicleDetailView.as_view(), name='vehicle_detail'),
    # path('vehicle/<int:vehicle_id>/reserve/', VehicleReservationView.as_view(), name='vehicle_reservation'),
]

from . import views

urlpatterns = [
    path('ratepools/', views.RatePoolListView.as_view(), name='ratepool-list'),
    path('ratepools/create/', views.RatePoolCreateView.as_view(), name='ratepool-create'),
    path('ratepools/<int:pk>/update/', views.RatePoolUpdateView.as_view(), name='ratepool-update'),
]

urlpatterns += [
    path('ratetypes/', views.RateTypeListView.as_view(), name='ratetype-list'),
    path('ratetypes/create/', views.RateTypeCreateView.as_view(), name='ratetype-create'),
    path('ratetypes/<int:pk>/update/', views.RateTypeUpdateView.as_view(), name='ratetype-update'),
    path('ratetypes/<int:pk>/delete/', views.RateTypeDeleteView.as_view(), name='ratetype-delete'),
]


# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
from .views import DayOfTheWeekListView

# router = DefaultRouter()
# router.register(r'days-of-the-week', DayOfTheWeekListCreateView, basename='dayoftheweek')

urlpatterns += [
    path('api/days-of-the-week', DayOfTheWeekListView.as_view(), name='dayoftheweek-detail'),
    path('api/days-of-the-week/<int:pk>/', DayOfTheWeekListView.as_view(), name='dayoftheweek-detail'),
]