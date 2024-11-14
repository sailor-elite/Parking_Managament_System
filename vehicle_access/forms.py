from django import forms


class VehicleSearchForm(forms.Form):
    license_plate = forms.CharField(max_length=10, label="Vehicle License Plate")
    zone = forms.ChoiceField(choices=[('greenZone', 'Green Zone'), ('redZone', 'Red Zone'), ('blueZone', 'Blue Zone')],
                             label="Select Zone")
