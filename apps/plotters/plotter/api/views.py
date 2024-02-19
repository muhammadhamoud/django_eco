from rest_framework.generics import ListAPIView
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import generics

from plotter.permissions import IsAuthenticated
from .serializers import CarSerializer
from rest_framework import generics
from django.shortcuts import get_object_or_404
from django.db.models import Q
from plotter.models import Car, Make, Model, Trim
from django.utils.text import slugify
from django.views.generic import ListView

from .serializers import CarSerializer

from plotter.models import Car, Files
from .serializers import *

class NoPagination(PageNumberPagination):
    page_size = None

class ApplicationListView(generics.ListAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    pagination_class = NoPagination 

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class ApplicationDetailView(generics.RetrieveAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    lookup_field = 'slug'
    pagination_class = NoPagination

    def retrieve(self, request, *args, **kwargs):
        if 'search' in request.GET:
            search_term = request.GET['search']
            queryset = self.queryset.filter(
                Q(name__icontains=search_term) | 
                Q(description__icontains=search_term)
            )
            instance = queryset.first()
        else:
            instance = self.get_object()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class BodyPartListView(generics.ListAPIView, generics.RetrieveAPIView):
    queryset = BodyPart.objects.all()
    serializer_class = BodyPartSerializer
    pagination_class = None  # Disable pagination for the list view

    def get(self, request, *args, **kwargs):
        search_term = request.GET.get('search', None)
        
        if search_term:
            return self.search(request, search_term)
        else:
            return super().get(request, *args, **kwargs)

    def search(self, request, search_term):
        queryset = self.queryset.filter(
            Q(translations__name__icontains=search_term) | 
            Q(translations__description__icontains=search_term)
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class BodyListView(generics.ListAPIView):
    queryset = Body.objects.all()
    serializer_class = BodySerializer
    pagination_class = NoPagination

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class MakeListView(generics.ListAPIView):
    queryset = Make.objects.all()
    serializer_class = MakeSerializer
    pagination_class = NoPagination 

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class ModelsListView(generics.ListAPIView):
    serializer_class = ModelSerializer
    pagination_class = NoPagination 

    def get_queryset(self):
        make_id = self.kwargs.get('make_id')
        make = get_object_or_404(Make, id=make_id)
        return Model.objects.filter(make=make)

class TrimsListView(generics.ListAPIView):
    serializer_class = TrimSerializer
    pagination_class = NoPagination 

    def get_queryset(self):
        model_id = self.kwargs.get('model_id')
        model = get_object_or_404(Model, id=model_id)
        return Trim.objects.filter(model=model)

class CarListView(ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

class CarFilterView(generics.ListAPIView):
    serializer_class = CarSerializer
    lookup_field = 'slug' 

    def get_queryset(self):
        # Search for a matching Car, Make, Model, or Trim based on the provided slug
        slug = self.kwargs.get('slug')
        car_queryset = Car.objects.filter(slug=slug)
        make_queryset = Make.objects.filter(slug=slug)
        model_queryset = Model.objects.filter(slug=slug)
        trim_queryset = Trim.objects.filter(slug=slug)

        # Combine the querysets
        queryset = car_queryset.union(make_queryset, model_queryset, trim_queryset)
        
        return queryset


# class CarSearchView(generics.ListAPIView):
#     serializer_class = CarSerializer
#     lookup_field = 'slug' 

#     def get_queryset(self):
#         # Search for a matching Car, Make, Model, or Trim based on the provided slug
#         search_term = self.kwargs.get('search_term')
#         search_term_slug = slugify(search_term)

#         # Create a queryset using regex for case-insensitive matching on slug and name
#         queryset = Car.objects.filter(
#             Q(slug__iregex=r'(\w+)'.format(search_term_slug)) 
#             | Q(translations__name__iregex=r'-(\w+)-'.format(search_term_slug)) 
#             | Q(slug__icontains=search_term_slug) | Q(translations__name__icontains=search_term_slug)
#         )

#         return queryset

class CarSearchView(generics.ListAPIView):
    serializer_class = CarSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        # Get the search term from URL parameters
        search_term = self.kwargs.get('search_term')
        
        # Split the search term into individual words
        search_words = search_term.split()

        # Create a queryset using regex for case-insensitive matching on slug and name
        queryset = Car.objects.all()

        # Iterate over each word in the search term and filter the queryset
        for word in search_words:
            search_word_slug = slugify(word)
            queryset = queryset.filter(
                Q(slug__iregex=r'(\b{0}\b)'.format(search_word_slug)) |
                Q(translations__name__iregex=r'-(\b{0}\b)-'.format(search_word_slug)) |
                Q(slug__icontains=search_word_slug) |
                Q(translations__name__icontains=search_word_slug)
            )
        return queryset.distinct()


class FilesListView(generics.ListAPIView):
    queryset = Files.objects.all()
    serializer_class = FilesSerializer
    # permission_classes = [IsAuthenticated, ]
    pagination_class = NoPagination 
    
    def get_queryset(self):
        queryset = Files.objects.all()

        # Get the car ID from query parameters
        car_id = self.request.query_params.get('car_id')

        # If car ID is provided, filter files by car ID
        if car_id:
            queryset = queryset.filter(car__id=car_id)

        return queryset


class FilesDetailView(generics.RetrieveAPIView):
    queryset = Files.objects.all()
    serializer_class = FilesSerializer
    lookup_field = 'slug'  


