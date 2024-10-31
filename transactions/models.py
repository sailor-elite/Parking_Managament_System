from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from parking.models import Parking


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
