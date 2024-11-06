from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
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


@receiver(post_save, sender=Transaction)
def trigger_open_barrier(sender, instance, created, **kwargs):
    if created:  # Runs only on creation, not updates
        open_barrier(instance)


# This function gets triggered each time when user enter the parking lot (transaction gets created)
# Kuba You need to implement Your logic for embedded controller here (for example trigger barrier open for 10seconds)
def open_barrier(transaction):
    print(f"Barrier opened for transaction {transaction.id} in zone {transaction.zone}")
