from django.db import models
from django.db.models import Count
from django.utils import timezone
from datetime import datetime


# Create your models here.

class Parking(models.Model):
    name = models.CharField(max_length=50, default="defaultParking")
    greenZoneSpaces = models.IntegerField(default=66)
    blueZoneSpaces = models.IntegerField(default=66)
    redZoneSpaces = models.IntegerField(default=66)

    def __str__(self):
        return self.name

    def get_available_spaces(self, zone):
        from transactions.models import Transaction

        zone_spaces = {
            'greenZone': self.greenZoneSpaces,
            'blueZone': self.blueZoneSpaces,
            'redZone': self.redZoneSpaces
        }.get(zone)

        if zone_spaces is None:
            raise ValueError(f"Invalid zone '{zone}' specified.")

        first_day_of_month = datetime.now().replace(day=1)

        zone_transactions = (
            Transaction.objects
            .filter(parking=self, zone=zone, transactionTimestamp__gte=first_day_of_month)
            .values('vehicle')
            .annotate(transaction_count=Count('id'))
        )

        occupied_spaces = sum(1 for entry in zone_transactions if entry['transaction_count'] % 2 != 0)

        available_spaces = zone_spaces - occupied_spaces

        return available_spaces
