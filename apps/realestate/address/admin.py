from django.contrib import admin
from .models import Country, City, AddressType, Address, AddressFormat, State

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    pass

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    pass

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    pass

@admin.register(AddressType)
class AddressTypeAdmin(admin.ModelAdmin):
    pass

@admin.register(AddressFormat)
class AddressFormatAdmin(admin.ModelAdmin):
    pass

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass