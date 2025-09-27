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
