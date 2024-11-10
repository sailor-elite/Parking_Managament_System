from rest_framework import serializers
from .models import Parking


class ParkingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parking
        fields = ['name', 'greenZoneSpaces', 'blueZoneSpaces', 'redZoneSpaces']
