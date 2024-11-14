from django import forms


class VehicleSearchForm(forms.Form):
    username = forms.CharField(max_length=150, label='Username')
    zone = forms.ChoiceField(choices=[('greenZone', 'Green Zone'), ('blueZone', 'Blue Zone'), ('redZone', 'Red Zone')])
