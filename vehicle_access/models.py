from django.db import models
from django.contrib.auth.models import User


class Zone(models.Model):
    name = models.CharField(max_length=50)
    access_code = models.CharField(max_length=2)

    def __str__(self):
        return self.name


User.add_to_class('zones', models.ManyToManyField(Zone, blank=True))
