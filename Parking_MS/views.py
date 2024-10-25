from django.shortcuts import render
from django.contrib.auth.models import User
from vehicles.models import Vehicle


# Create your views here.

def home(request):
    return render(request, 'home.html', {})


def stats(request):
    # vehicles = Vehicle.objects.all()
    # users = User.objects.all()
    vehicles = Vehicle.objects.prefetch_related('owners').all()
    users = User.objects.prefetch_related('vehicles').all()

    return render(request, 'stats.html', {'vehicles': vehicles, 'users': users})
