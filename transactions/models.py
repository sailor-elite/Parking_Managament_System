from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from parking.models import Parking

import serial
import glob
import sys


# Create your models here.

class Transaction(models.Model):
    class ZoneChoices(models.TextChoices):
        GREEN = 'greenZone', 'Green Zone'
        BLUE = 'blueZone', 'Blue Zone'
        RED = 'redZone', 'Red Zone'

    vehicle = models.ForeignKey('vehicles.Vehicle', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    transactionTimestamp = models.DateTimeField(default=timezone.now)
    parking = models.ForeignKey(Parking, on_delete=models.CASCADE, related_name='transactions')
    zone = models.CharField(max_length=10, choices=ZoneChoices.choices)

    def __str__(self):
        return self.vehicle.licensePlate + " " + self.user.username + " " + self.zone

    def ready(self):
        self.serial_ports = self.init_serial_ports()

    @staticmethod
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
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result


@receiver(post_save, sender=Transaction)
def trigger_open_barrier(sender, instance, created, **kwargs):
    if created:  # Runs only on creation, not updates
        open_barrier(instance)


# This function gets triggered each time when user enter the parking lot (transaction gets created)

def ser_write(ser, command, selected_port):
    ser.write(command.encode())
    print(f"send to {selected_port} message: {command}")
    ser.close()


def open_barrier(transaction):
    ports = transaction.init_serial_ports()
    if not ports:
        print("No serial ports found!")
        return
    elif ports:
        selected_port = ports[0]
        ser = serial.Serial(selected_port, baudrate=115200, timeout=1)
        print(f"connected to {selected_port}")
    print(f"Barrier opened for transaction {transaction.id} in zone {transaction.zone}")
    if transaction.zone in ['greenZone', 'Green Zone'] and ports:

        try:
            command = "11"
            ser_write(ser, command, selected_port)

        except serial.SerialException as e:
            print(f"Error communicating with serial port: {e}")

    elif transaction.zone in ['redZone', 'Red Zone'] and ports:

        try:
            command = "21"
            ser_write(ser, command, selected_port)

        except serial.SerialException as e:
            print(f"Error communicating with serial port: {e}")

    elif transaction.zone in ['blueZone', 'Blue Zone'] and ports:

        try:
            command = "31"
            ser_write(ser, command, selected_port)

        except serial.SerialException as e:
            print(f"Error communicating with serial port: {e}")
