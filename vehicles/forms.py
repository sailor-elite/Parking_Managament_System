from django import forms
from .models import Vehicle


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['licensePlate', 'make', 'model']
        labels = {
            'licensePlate': 'License Plate',
        }
