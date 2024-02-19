from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from address.models import Country, City, Address, State, AddressType, AddressFormat
from .serializers import (
    CountrySerializer, 
    CitySerializer, 
    AddressCreateSerializer, 
    AddressViewSerializer, 
    StateSerializer, 
    AddressTypeSerializer
)

class CountryListView(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

class CityListView(generics.ListAPIView):
    # queryset = City.objects.all()
    serializer_class = CitySerializer

    def get_queryset(self):
        country_id = self.request.query_params.get('country')
        if country_id:
            return City.objects.filter(country=country_id)
        else:
            return City.objects.all()

class StateListView(APIView):
    serializer_class = StateSerializer

    def get(self, request, *args, **kwargs):
        country_id = self.request.query_params.get('country')

        try:
            country_id = int(country_id)
            states = State.objects.filter(country=country_id)
            serialized_data = self.serializer_class(states, many=True).data
            return Response(serialized_data)
        
        except (ValueError, TypeError):
            # Handle the case where the country_id is not a valid integer
            return Response({"error": "Invalid country ID"}, status=400)

class AddressTypeListView(APIView):
    def get(self, request, *args, **kwargs):
        address_types = AddressType.objects.all()
        serializer = AddressTypeSerializer(address_types, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# class AddressListView(generics.ListCreateAPIView):
#     queryset = Address.objects.all()
#     permission_classes = (permissions.IsAuthenticated,)

#     def get_serializer_class(self):
#         if self.request.method == 'POST':
#             return AddressCreateSerializer
#         return AddressViewSerializer




class AddressListView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddressCreateSerializer
        return AddressViewSerializer

    def get_queryset(self):
        # Filter addresses for the authenticated user
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically associate the authenticated user with the address
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        # Ensure that the Authorization header is present in the request
        if 'Authorization' not in request.headers:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

        # Ensure that the user is authenticated
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication credentials are not valid.'}, status=status.HTTP_401_UNAUTHORIZED)

        # Access the authenticated user via request.user
        authenticated_user = request.user

        # Your existing post method logic here
        return super().post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # Ensure that the Authorization header is present in the request
        if 'Authorization' not in request.headers:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

        # Ensure that the user is authenticated
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication credentials are not valid.'}, status=status.HTTP_401_UNAUTHORIZED)

        # Access the authenticated user via request.user
        authenticated_user = request.user

        # Your existing get method logic here
        return super().get(request, *args, **kwargs)
    


