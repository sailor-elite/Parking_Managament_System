from django.shortcuts import render
from .forms import VehicleSearchForm
from .models import Vehicle, Zone, VehicleAccess
from serial import Serial, SerialException
import glob


def search_vehicle(request):
    if request.method == 'POST':
        form = VehicleSearchForm(request.POST)
        if form.is_valid():
            license_plate = form.cleaned_data['license_plate']
            zone_name = form.cleaned_data['zone']
            print(license_plate, zone_name)
            try:
                print("jestem tu")
                vehicle = Vehicle.objects.get(license_plate=license_plate)
                print(vehicle)
                zone = Zone.objects.get(name=zone_name)
                access = VehicleAccess.objects.filter(vehicle=vehicle, zone=zone).exists()
                if access:
                    command = get_serial_command_for_zone(zone_name)
                    send_command_to_serial_port(command)
                    message = "Access granted. Command sent to serial port."
                else:
                    message = "Vehicle does not have access to this zone."
            except Vehicle.DoesNotExist:
                message = "Vehicle not found."
            except Zone.DoesNotExist:
                message = "Zone not found."
        else:
            message = "Invalid form data."

        return render(request, 'vehicle_access/search_vehicle.html', {'form': form, 'message': message})
    else:
        form = VehicleSearchForm()
    return render(request, 'vehicle_access/search_vehicle.html', {'form': form})


def get_serial_command_for_zone(zone_name):
    zone_commands = {
        'greenZone': "11",
        'greenZoneNoAccess': "10",
        'redZone': "21",
        'redZoneNoAccess': "20",
        'blueZone': "31",
        'blueZoneNoAccess': "30"

    }
    return zone_commands.get(zone_name, "00")


def send_command_to_serial_port(command):
    ports = glob.glob('/dev/tty[A-Za-z]*')  # Wyszukiwanie portów
    if ports:
        selected_port = ports[0]  # Wybór pierwszego portu
        try:
            with Serial(selected_port, baudrate=115200, timeout=1) as ser:
                ser.write(command.encode())
                print(f"Sent command '{command}' to {selected_port}")
        except SerialException as e:
            print(f"Error communicating with serial port: {e}")
