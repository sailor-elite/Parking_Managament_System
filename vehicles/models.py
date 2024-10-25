from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Vehicle(models.Model):
    licensePlate = models.CharField(max_length=40, unique=True)
    make = models.CharField(max_length=40)
    model = models.CharField(max_length=40, blank=True)
    owners = models.ManyToManyField(User, related_name='vehicles')

    def __str__(self):
        return self.licensePlate
