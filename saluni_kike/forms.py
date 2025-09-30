# saluni_kike/forms.py
from django import forms
from .models import Salon

class SalonForm(forms.ModelForm):
    class Meta:
        model = Salon
        fields = ['name', 'phone']  # field chache tu
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Jina la saluni'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Namba ya simu'}),
        }


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# saluni_kike/forms.py
from .models import Salon
from django import forms

class SalonProfileForm(forms.ModelForm):
    class Meta:
        model = Salon
        fields = [
            'description', 'address', 'region', 'district', 'street',
            'phone', 'email', 'website', 'facebook', 'instagram',
            'latitude', 'longitude'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows':3}),
        }


################################################################################

# bookings/forms.py
from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['service', 'stylist', 'start_datetime', 'notes']
        widgets = {
            'start_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        salon = kwargs.pop('salon', None)  # pop the salon instance
        super().__init__(*args, **kwargs)

        if salon:
            # Filter only services/stylists of this salon
            self.fields['service'].queryset = salon.services.all()
            self.fields['stylist'].queryset = salon.stylists.all()
        else:
            self.fields['service'].queryset = Booking.objects.none()
            self.fields['stylist'].queryset = Booking.objects.none()
