from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from parking.models import Parking
from transactions.forms import TransactionForm
from transactions.models import Transaction
from transactions.serializers import TransactionSerializer
from vehicles.models import Vehicle


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def transactions_view(request):
    is_api_request = request.content_type == 'application/json'
    if is_api_request:
        user_transactions = Transaction.objects.filter(user=request.user)
        serializer = TransactionSerializer(user_transactions, many=True)
        return Response({'transactions': serializer.data})

    transactions = Transaction.objects.all()
    return render(request, 'transactions.html', {'transactions': transactions})


@csrf_exempt
@permission_classes([IsAuthenticated])
def add_transaction(request):
    if request.method == 'POST':
        is_api_request = request.content_type == 'application/json'
        if is_api_request:
            return handle_api_transaction(request)
        else:
            return handle_web_transaction(request)

    form = TransactionForm(user=request.user)
    return render(request, 'add_transaction.html', {'form': form})


def handle_web_transaction(request):
    print("handle_web_transaction")
    form = TransactionForm(request.POST, user=request.user)
    if form.is_valid():
        transaction = form.save(commit=False)
        transaction.user = request.user
        transaction.save()
        return redirect('home')
    else:
        return render(request, 'add_transaction.html', {'form': form})


@api_view(['POST'])
def handle_api_transaction(request):
    print("handle_api_transaction")
    user = request.user
    data = request.data

    vehicle_license_plate = data.get('vehicle')
    parking_name = data.get('parking')

    try:
        vehicle = Vehicle.objects.get(licensePlate=vehicle_license_plate)
    except Vehicle.DoesNotExist:
        return Response({'status': 'error', 'message': 'Vehicle not found'}, status=404)

    try:
        parking = Parking.objects.get(name=parking_name)
    except Parking.DoesNotExist:
        return Response({'status': 'error', 'message': 'Parking not found'}, status=404)

    form_data = {**data, 'vehicle': vehicle, 'parking': parking}
    form = TransactionForm(form_data, user=user)

    if form.is_valid():
        form.save()
        return Response({'status': 'success'})
    else:
        return Response({'status': 'error', 'errors': form.errors}, status=400)
