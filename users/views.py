from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from parking.models import Parking
from users.forms import SignUpForm
from vehicles.models import Vehicle


# Create your views here.

def register_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            login(request, form.save())
            return redirect("home")
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect("home")


# TODO: Here we should return only access and refresh token
#  So later we should delete all extra user info which is returned now
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
        data['vehicles'] = [f"{vehicle.licensePlate} {vehicle.make} {vehicle.model}" for vehicle in vehicles]

        parking_names = Parking.objects.values_list('name', flat=True)
        data['parkings'] = list(parking_names)

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
