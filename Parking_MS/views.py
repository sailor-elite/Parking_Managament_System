from django.shortcuts import render
from django.contrib.auth.models import User

from parking.models import Parking
from vehicles.models import Vehicle


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
    # vehicles = Vehicle.objects.all()
    # users = User.objects.all()
    vehicles = Vehicle.objects.prefetch_related('owners').all()
    users = User.objects.prefetch_related('vehicles').all()

    return render(request, 'stats.html', {'vehicles': vehicles, 'users': users})
