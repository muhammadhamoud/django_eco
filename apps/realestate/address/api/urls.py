from django.urls import path
from .views import CountryListView, CityListView, AddressListView, StateListView

urlpatterns = [
    path('countries/', CountryListView.as_view(), name='country-list'),
    path('cities/', CityListView.as_view(), name='city-list'),
    path('states/', StateListView.as_view(), name='state-list'),
    path('addresses/', AddressListView.as_view(), name='address-list'),
]