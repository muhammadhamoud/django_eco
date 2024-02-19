from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, DetailView
from .models import RatePool

from django.views.generic import ListView
from .models import RatePool

class RatePoolListView(ListView):
    model = RatePool
    template_name = 'ratepool_list.html' 
    context_object_name = 'ratepools' 


class RatePoolCreateView(CreateView):
    model = RatePool
    template_name = 'ratepool_form.html'  # Create an HTML template for the create form
    fields = ['code', 'name', 'quantity']  # Specify the fields you want to include in the form


class RatePoolUpdateView(UpdateView):
    model = RatePool
    template_name = 'ratepool_form.html'  # Use the same form template as for creating
    fields = ['code', 'name', 'quantity']  # Specify the fields you want to include in the form


class RatePoolEditView(CreateView, UpdateView):
    model = RatePool
    template_name = 'ratepool_form.html'  # Use the same form template as for create and update
    fields = ['code', 'name', 'quantity']  # Specify the fields you want to include in the form


from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import RateType
from .forms import RateTypeForm
from django.urls import reverse_lazy

class RateTypeListView(ListView):
    model = RateType
    template_name = 'ratetype_list.html'
    context_object_name = 'ratetypes'

class RateTypeCreateView(CreateView):
    model = RateType
    form_class = RateTypeForm
    template_name = 'ratetype_form.html'
    success_url = reverse_lazy('ratetype-list')

class RateTypeUpdateView(UpdateView):
    model = RateType
    form_class = RateTypeForm
    template_name = 'ratetype_form.html'
    success_url = reverse_lazy('ratetype-list')

class RateTypeDeleteView(DeleteView):
    model = RateType
    template_name = 'ratetype_confirm_delete.html'
    success_url = reverse_lazy('ratetype-list')


from rest_framework import generics
from rest_framework import permissions
from .serializers import DayOfTheWeekSerializer
from .models import DayOfTheWeek

class DayOfTheWeekListView(generics.ListAPIView):
    serializer_class = DayOfTheWeekSerializer
    queryset = DayOfTheWeek.objects.all()
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)

    def get_queryset(self):
        return DayOfTheWeek.objects.all() #self.queryset
    
    def get(self, request, *args, **kwargs):
        context = {
            'object_list': self.get_queryset(),
        }
        return render(request, 'day_of_the_week_list.html', context)
