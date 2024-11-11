from django.shortcuts import render, redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .forms import VehicleForm
from .models import Vehicle
from .serializers import VehicleSerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def vehicles_view(request):
    is_api_request = request.content_type == 'application/json'

    if request.method == 'GET':
        if is_api_request:
            user_vehicles = Vehicle.objects.filter(owners=request.user)
            serializer = VehicleSerializer(user_vehicles, many=True)
            return Response({'vehicles': serializer.data})
        else:
            form = VehicleForm()
            return render(request, 'vehicles.html', {'form': form})

    elif request.method == 'POST':
        if is_api_request:
            data = request.data
            serializer = VehicleSerializer(data=data)
            if serializer.is_valid():
                vehicle = serializer.save()
                vehicle.owners.set([request.user])
                return Response({'status': 'success', 'vehicle': serializer.data}, status=201)
            else:
                return Response({'status': 'error', 'errors': serializer.errors}, status=400)
        else:
            form = VehicleForm(request.POST)
            if form.is_valid():
                vehicle = form.save(commit=False)
                vehicle.save()
                vehicle.owners.set([request.user])
                return redirect('vehicles:vehicles')
            else:
                return render(request, 'vehicles.html', {'form': form})
