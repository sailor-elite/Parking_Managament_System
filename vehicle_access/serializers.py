from rest_framework import serializers


class VehicleAccessRequestSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    zone = serializers.ChoiceField(choices=['greenZone', 'blueZone', 'redZone'])
