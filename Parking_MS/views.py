from django.contrib.auth import authenticate
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

from parking.models import Parking
from parking.serializers import ParkingSerializer
from vehicles.models import Vehicle
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from vehicles.serializers import VehicleSerializer


# Create your views here.

def home(request):
    parking = Parking.objects.first()
    available_green_spaces = parking.get_available_spaces('greenZone')
    available_blue_spaces = parking.get_available_spaces('blueZone')
    available_red_spaces = parking.get_available_spaces('redZone')

    context = {
        'parking': parking,
        'available_green_spaces': available_green_spaces,
        'available_blue_spaces': available_blue_spaces,
        'available_red_spaces': available_red_spaces,
    }

    return render(request, 'home.html', context)


def stats(request):
    vehicles = Vehicle.objects.prefetch_related('owners').all()
    users = User.objects.prefetch_related('vehicles').all()

    return render(request, 'stats.html', {'vehicles': vehicles, 'users': users})


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        user = self.user
        data['userId'] = user.id
        data['username'] = user.username
        data['email'] = user.email
        data['firstName'] = user.first_name
        data['lastName'] = user.last_name

        # serialize Vehicles -> add to response
        vehicles = Vehicle.objects.filter(owners=user)
        vehicle_serializer = VehicleSerializer(vehicles, many=True)
        data['vehicles'] = vehicle_serializer.data

        # serialize Parkings -> add to response
        parkings = Parking.objects.all()
        parking_serializer = ParkingSerializer(parkings, many=True)
        data['parkings'] = parking_serializer.data

        group_zone_access = {
            'STUDENT': ['greenZone'],
            'TEACHER': ['blueZone'],
            'MANAGEMENT': ['redZone'],
            'TECHNICIAN': ['greenZone', 'blueZone', 'redZone']
        }

        # TODO: It should be handled way better than that:
        user_groups = user.groups.values_list('name', flat=True)

        data['userGroups'] = user_groups

        accessible_zones = set()
        for group in user_groups:
            accessible_zones.update(group_zone_access.get(group, []))

        data['accessibleZones'] = accessible_zones

        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
