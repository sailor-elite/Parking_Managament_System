from django import forms
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from vehicles.models import Vehicle
from .models import Transaction


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['vehicle', 'parking', 'zone']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        self.fields['vehicle'].queryset = Vehicle.objects.filter(owners=user)

        # define groups and accessible zones for them
        group_zone_access = {
            'STUDENT': ['greenZone'],
            'TEACHER': ['blueZone'],
            'MANAGEMENT': ['redZone'],
            'TECHNICIAN': ['greenZone', 'blueZone', 'redZone']
        }

        user_groups = user.groups.values_list('name', flat=True)

        accessible_zones = set()
        for group in user_groups:
            accessible_zones.update(group_zone_access.get(group, []))

        self.fields['zone'].choices = [
            (code, label) for code, label in self.fields['zone'].choices
            if code in accessible_zones
        ]
