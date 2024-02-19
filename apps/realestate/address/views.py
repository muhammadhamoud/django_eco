from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy

from .models import Country, City
from .forms import CountryAddressForm
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Address

class CountryAddressListView(ListView):
    model = Address
    context_object_name = 'address'

class CountryAddressCreateView(CreateView):
    model = Address
    form_class = CountryAddressForm
    fields = ('name', 'country', 'city')
    success_url = reverse_lazy('countryaddress_changelist')

class CountryAddressUpdateView(UpdateView):
    model = Address
    form_class = CountryAddressForm
    fields = ('name', 'country', 'city')
    success_url = reverse_lazy('countryaddress_changelist')


def load_cities(request):
    country_id = request.GET.get('country')
    cities = City.objects.filter(country_id=country_id).order_by('name')
    return render(request, 'city_dropdown_list_options.html', {'cities': cities})