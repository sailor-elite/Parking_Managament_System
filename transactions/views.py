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

from serial import SerialException
from serial import Serial
import sys
import glob


def init_serial_ports():
    """Lists serial port names."""
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = Serial(port)
            s.close()
            result.append(port)
        except (OSError, SerialException):
            pass
    return result


def ser_write(ser, command, selected_port):
    ser.write(command.encode())
    print(f"send to {selected_port} message: {command}")
    ser.close()


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

        ports = transaction.init_serial_ports()
        if not ports:
            print("No serial ports found!")
        else:
            selected_port = ports[0]
            try:
                ser = Serial(selected_port, baudrate=115200, timeout=1)
                print(f"Connected to {selected_port}")

                if transaction.zone in ['greenZone', 'Green Zone']:
                    command = "11"
                elif transaction.zone in ['blueZone', 'Blue Zone']:
                    command = "21"
                elif transaction.zone in ['redZone', 'Red Zone']:
                    command = "31"
                else:
                    print("Unknown zone")
                    ser.close()
                    return

                ser_write(ser, command, selected_port)

            except SerialException as e:
                print(f"Error communicating with serial port: {e}")

        return redirect('home')
    else:
        return render(request, 'add_transaction.html', {'form': form})


@csrf_exempt
@api_view(['POST'])
def handle_api_transaction(request):
    print("handle_api_transaction")
    user = request.user
    data = request.data

    vehicle_license_plate = data.get('vehicle')
    parking_name = data.get('parking')

    print(data)

    try:
        vehicle = Vehicle.objects.get(licensePlate=vehicle_license_plate)
    except Vehicle.DoesNotExist:
        print("Vehicle not found")
        return Response({'status': 'error', 'message': 'Vehicle not found'}, status=404)
    try:
        parking = Parking.objects.get(name=parking_name)
    except Parking.DoesNotExist:
        print("Parking not found")
        return Response({'status': 'error', 'message': 'Parking not found'}, status=404)

    form_data = {**data, 'vehicle': vehicle, 'parking': parking}

    print(form_data)

    form = TransactionForm(form_data, user=user)

    if form.is_valid():
        transaction = form.save()

        ports = transaction.init_serial_ports()
        if not ports:
            print("No serial ports found!")
        else:
            selected_port = ports[0]
            try:
                ser = Serial(selected_port, baudrate=115200, timeout=1)
                print(f"Connected to {selected_port}")

                if transaction.zone in ['greenZone', 'Green Zone']:
                    command = "11"
                elif transaction.zone in ['blueZone', 'Blue Zone']:
                    command = "21"
                elif transaction.zone in ['redZone', 'Red Zone']:
                    command = "31"
                else:
                    print("Unknown zone")
                    ser.close()
                    return Response({'status': 'error', 'message': 'Unknown zone'}, status=400)

                ser_write(ser, command, selected_port)

            except SerialException as e:
                print(f"Error communicating with serial port: {e}")

        return Response({'status': 'success'})
    else:
        return Response({'status': 'error', 'errors': form.errors}, status=400)
