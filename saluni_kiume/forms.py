
from django import forms
from .models import MaleSalon

class MaleSalonForm(forms.ModelForm):
    class Meta:
        model = MaleSalon
        fields = ['name', 'phone']  # minimal fields
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Jina la saluni'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Namba ya simu'}),
        }



from django import forms
from .models import MaleSalon

class SalonProfileForm(forms.ModelForm):
    class Meta:
        model = MaleSalon
        fields = [
            'name', 'phone', 'address', 'region', 'district',
            'street', 'email', 'website', 'latitude', 'longitude'
        ]
        widgets = {
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }
