from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from serial import SerialException
from serial import Serial
from parking.models import Parking
import datetime
import pytz

# import Serial
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
