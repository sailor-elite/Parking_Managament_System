from django import forms
from .models import Vehicle


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['licensePlate', 'make', 'model', 'vehicle_photo']
        labels = {
            'licensePlate': 'License Plate',
        }
