from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from parking.models import Parking
from vehicles.models import Vehicle


# Create your views here.

def home(request):
    parking = Parking.objects.first()

    if parking is None:
        available_green_spaces = 0
        available_blue_spaces = 0
        available_red_spaces = 0
    else:
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
