# saluni_kike/forms.py
from django import forms
from .models import Salon
from django.core.exceptions import ValidationError

# Validators for GPS
def validate_latitude(value):
    if value is None:
        return
    if not (-90 <= value <= 90):
        raise ValidationError('Latitude must be between -90 and 90.')

def validate_longitude(value):
    if value is None:
        return
    if not (-180 <= value <= 180):
        raise ValidationError('Longitude must be between -180 and 180.')

class SalonForm(forms.ModelForm):
    # Hidden GPS fields
    latitude = forms.DecimalField(
        max_digits=9, decimal_places=6,
        required=False,
        validators=[validate_latitude],
        widget=forms.HiddenInput()
    )
    longitude = forms.DecimalField(
        max_digits=9, decimal_places=6,
        required=False,
        validators=[validate_longitude],
        widget=forms.HiddenInput()
    )

    # New fields for location breakdown
    region = forms.CharField(max_length=100, required=True)
    district = forms.CharField(max_length=100, required=True)
    street = forms.CharField(max_length=200, required=True)

    class Meta:
        model = Salon
        fields = [
            'name', 'description', 'phone', 'email', 'website',
            'address', 'region', 'district', 'street',
            'latitude', 'longitude'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows':3}),
        }
