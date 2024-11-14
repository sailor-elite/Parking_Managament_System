from django.db import models


class Vehicle(models.Model):
    license_plate = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.license_plate


class Zone(models.Model):
    name = models.CharField(max_length=50)
    access_code = models.CharField(max_length=2)

    def __str__(self):
        return self.name


class VehicleAccess(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.vehicle} - {self.zone}"
