from django.db import models
from django_countries.fields import CountryField
from django.conf import settings
from django_countries import Countries
from django.utils.translation import gettext_lazy as _
from core.models import TimeStampedModel

class CountriesOnly(Countries):
    only = ["SA", "AE", "US"]

class Country(models.Model):
    # country = CountryField(blank_label="(select country)", countries=CountriesOnly, unique=True)
    country = CountryField(blank_label="(select country)", unique=True)
    
    @property
    def name(self):
        name = self.country.name
        return name

    def __str__(self):
        return f"{self.country}"
    
    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")

class City(models.Model):
    name = models.CharField(max_length=50, unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, related_name='cities')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = _("City")
        verbose_name_plural = _("Cities")

class State(models.Model):
    name = models.CharField(max_length=50, unique=True)
    abbreviation = models.CharField(max_length=2)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, related_name='states')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = _("State")
        verbose_name_plural = _("States")

class AddressType(models.Model):
    HOME = 'Home'
    WORK = 'Work'
    BILLING = 'Billing'
    DELIVERY = 'Delivery'
    MAIN = 'Main'

    TYPE_CHOICES = [
        (HOME, _('Home')),
        (WORK, _('Work')),
        (BILLING, _('Billing')),
        (DELIVERY, _('Delivery')),
        (MAIN, _('Main')),
    ]
    type = models.CharField(_("Address Type"), max_length=255, choices=TYPE_CHOICES, unique=True)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = _("Address Type")
        verbose_name_plural = _("Address Types")

class AddressFormat(models.Model):
    name = models.CharField(_("Name"), max_length=50, unique=True)
    format = models.PositiveSmallIntegerField(_("Format"), default=1)
    
    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name = _("Address Format")
        verbose_name_plural = _("Address Formats")

class Address(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    type = models.ForeignKey(
        AddressType, on_delete=models.SET_NULL, null=True
        # , default=AddressType.objects.get(type=AddressType.MAIN)
    )
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    format = models.ForeignKey(AddressFormat, on_delete=models.SET_NULL, null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)

    company = models.TextField(_("Company"), blank=True, null=True)
    full_name = models.TextField(_("Full Name"), blank=True, null=True)
    
    street = models.TextField(_("Street Address"))
    additional = models.TextField(_("Additional Address"), blank=True, null=True)
    postal_code = models.CharField(_("Postal Code"), max_length=20, blank=True, null=True)

    building_number = models.PositiveSmallIntegerField(_("Building Number"), blank=True, null=True)
    apartment_number = models.PositiveSmallIntegerField(_("Apartment Number"), blank=True, null=True)
    primary = models.BooleanField(_("Primary Address"), default=False)

    def __str__(self):
        return f'{self.street}, {self.city}, {self.state} {self.postal_code}, {self.country}'
    
    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")
        ordering = ["-modified"]
        unique_together = ['user', 'type']

