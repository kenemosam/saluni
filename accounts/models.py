# accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

PHONE_REGEX = RegexValidator(
    regex=r'^\+?[0-9]{9,15}$',
    message="Nambari ya simu lazima iwe katika muundo: '+999999999'. Mitego hadi tarakimu 15."
)

class Customer(AbstractUser):
    ROLE_CHOICES = (
        ('customer', 'Mteja'),                      # customer -> "Mteja"
        ('owner', 'Mmiliki'),             # owner -> "Mmiliki wa saluni"
        ('barber', 'Barber / Kinyozi'),             # barber -> label includes Swahili + English
        ('hairdresser', 'Msusi'),     # hairdresser -> "Mchongaji wa nywele"
        ('admin', 'Msimamizi'),             # admin -> "Msimamizi"
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')

    phone = models.CharField(validators=[PHONE_REGEX], max_length=16, blank=True, null=True)
    is_phone_verified = models.BooleanField(default=False)
    profile_image = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.get_full_name() or self.username
from django.db import models

# Create your models here.
