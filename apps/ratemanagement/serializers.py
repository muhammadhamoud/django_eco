from rest_framework import serializers
from .models import DayOfTheWeek

class DayOfTheWeekSerializer(serializers.ModelSerializer):
    class Meta:
        model = DayOfTheWeek
        fields = '__all__'  # Serialize all fields from the DayOfTheWeek model