from django.urls import path, include
from . import views

urlpatterns = [
    path('address/', views.CountryAddressListView.as_view(), name='countryaddress_changelist'),
    path('address/add/', views.CountryAddressCreateView.as_view(), name='CountryAddress_add'),
    path('address/<int:pk>/', views.CountryAddressUpdateView.as_view(), name='CountryAddress_change'),

    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),  # <-- this one here

]