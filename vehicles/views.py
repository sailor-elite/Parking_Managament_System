from django.shortcuts import render, redirect
from .forms import VehicleForm
from django.contrib.auth.decorators import login_required

from .models import Vehicle


# Create your views here.

# def vehicles_view(request):
#     # form = VehicleForm()
#     # user_vehicles = Vehicle.objects.filter(owner=request.user)
#     # return render(request, 'vehicles.html', 'user_v')
#     return render(request, 'vehicles.html', {'form': form, 'user_vehicles': user_vehicles})


@login_required
def vehicles_view(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.save()
            vehicle.owners.set([request.user])
            return redirect('vehicles:vehicles')
    else:
        form = VehicleForm()

    return render(request, 'vehicles.html', {'form': form})
