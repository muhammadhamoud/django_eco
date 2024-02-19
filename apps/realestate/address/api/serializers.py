from django_countries.serializer_fields import CountryField
from rest_framework import serializers

class CountrySerializer(serializers.Serializer):
    country = CountryField(name_only=True)

from django_countries.serializers import CountryFieldMixin
# class CountrySerializer(CountryFieldMixin, serializers.ModelSerializer):
#     pass

from rest_framework import serializers
from address.models import Country, City, Address, AddressType, AddressFormat, State

class CountrySerializer(CountryFieldMixin,serializers.ModelSerializer):
    name = serializers.ReadOnlyField()
    country_info = serializers.SerializerMethodField()

    class Meta:
        model = Country
        fields = '__all__'

    def get_country_info(self, obj):
        return {
            'code': obj.country.alpha3,
            'flag': obj.country.flag,
            'flag_css': obj.country.flag_css,
            'numeric': obj.country.numeric,
        }

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'name', 'country')

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'

class AddressTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressType
        fields = '__all__'

class AddressFormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressFormat
        fields = '__all__'

class AddressViewSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    city = CitySerializer()
    type = AddressTypeSerializer()
    format = AddressFormatSerializer()
    state = StateSerializer()

    class Meta:
        model = Address
        fields = '__all__'


class AddressCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
        read_only_fields = ['user']

    def validate(self, data):
        user = self.context['request'].user
        address_type = data.get('type')
        
        # Check if a user already has an address with the same type
        address_exists = Address.objects.filter(user=user, type=address_type).exists()

        if address_exists:
            raise serializers.ValidationError({
                'error': ['User already has an address with the same type.']
            })


        return data

    def create(self, validated_data):
        # Automatically set the user during creation
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
