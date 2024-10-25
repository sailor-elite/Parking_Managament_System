from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Transaction(models.Model):
    vehicle = models.ForeignKey('vehicles.Vehicle', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    entryTime = models.DateTimeField(auto_now_add=True)
    exitTime = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.vehicle.licensePlate + " " + self.user.username
