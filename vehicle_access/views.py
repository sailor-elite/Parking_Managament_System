from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .forms import VehicleSearchForm
from django.contrib.auth.models import User
from serial import Serial, SerialException
import glob
import sys
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from vehicles.models import Vehicle
from django.contrib.auth.models import User

from .serializers import VehicleAccessRequestSerializer

GROUP_ZONE_ACCESS = {
    'STUDENT': ['greenZone'],
    'TEACHER': ['blueZone'],
    'MANAGEMENT': ['redZone'],
    'TECHNICIAN': ['greenZone', 'blueZone', 'redZone']
}


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


def get_serial_command_for_zone(zone_name, access_granted):
    zone_commands = {
        'greenZone': ("11", "10"),
        'blueZone': ("21", "20"),
        'redZone': ("31", "30")
    }

    access_command = zone_commands.get(zone_name, ("00", "00"))
    return access_command[0] if access_granted else access_command[1]


def send_command_to_serial_port(command):
    ports = init_serial_ports()
    if ports:
        selected_port = ports[0]
        try:
            with Serial(selected_port, baudrate=115200, timeout=1) as ser:
                ser.write(command.encode())
                print(f"Sent command '{command}' to {selected_port}")
        except SerialException as e:
            print(f"Error communicating with serial port: {e}")
    else:
        print("No serial ports found!")


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def vehicle_access_api(request):
    """Handles vehicle access request from API."""
    serializer = VehicleAccessRequestSerializer(data=request.data)

    if serializer.is_valid():
        username = serializer.validated_data['username']
        zone_name = serializer.validated_data['zone']

        try:
            user = User.objects.get(username=username)
            user_groups = user.groups.values_list('name', flat=True)

            accessible_zones = set()
            for group in user_groups:
                zones = GROUP_ZONE_ACCESS.get(group, [])
                accessible_zones.update(zones)

            if zone_name in accessible_zones:
                command = get_serial_command_for_zone(zone_name, access_granted=True)
                send_command_to_serial_port(command)
                return Response({"message": "Access granted. Command sent to serial port."}, status=200)
            else:
                command = get_serial_command_for_zone(zone_name, access_granted=False)
                send_command_to_serial_port(command)
                return Response({"message": "User does not have access to this zone. Command sent for no access."},
                                status=200)

        except User.DoesNotExist:
            return Response({"message": "User not found."}, status=404)
    return Response(serializer.errors, status=400)


@csrf_exempt
@permission_classes([IsAuthenticated])
def vehicle_access_web(request):
    """Handles vehicle access request from web form."""
    if request.method == 'POST':
        form = VehicleSearchForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            zone_name = form.cleaned_data['zone']

            try:
                user = User.objects.get(username=username)
                user_groups = user.groups.values_list('name', flat=True)

                accessible_zones = set()
                for group in user_groups:
                    zones = GROUP_ZONE_ACCESS.get(group, [])
                    accessible_zones.update(zones)

                if zone_name in accessible_zones:
                    command = get_serial_command_for_zone(zone_name, access_granted=True)
                    send_command_to_serial_port(command)
                    message = "Access granted. Command sent to serial port."
                else:
                    command = get_serial_command_for_zone(zone_name, access_granted=False)
                    send_command_to_serial_port(command)
                    message = "User does not have access to this zone. Command sent for no access."
            except User.DoesNotExist:
                message = "User not found."
            return render(request, 'vehicle_access/search_vehicle.html', {'form': form, 'message': message})

    else:
        form = VehicleSearchForm()

    return render(request, 'vehicle_access/search_vehicle.html', {'form': form})
