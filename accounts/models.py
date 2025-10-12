from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator

PHONE_REGEX = RegexValidator(
    regex=r'^\+?[0-9]{9,15}$',
    message="Nambari ya simu lazima iwe katika muundo: '+999999999'. Mitego hadi tarakimu 15."
)

# ----------------------------
# Custom user manager
# ----------------------------
class CustomerManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError("The Phone number must be set")
        phone = self.normalize_email(phone)  # optional: normalize if using email-like phone
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(phone, password, **extra_fields)


# ----------------------------
# Custom user model
# ----------------------------
class Customer(AbstractUser):
    ROLE_CHOICES = (
        ('customer', 'Mteja'),
        ('owner', 'Mmiliki'),
        ('barber', 'Barber / Kinyozi'),
        ('hairdresser', 'Msusi'),
        ('admin', 'Msimamizi'),
    )

    username = None  # remove username field
    phone = models.CharField(validators=[PHONE_REGEX], max_length=16, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    is_phone_verified = models.BooleanField(default=False)
    profile_image = models.URLField(blank=True, null=True)

    # set phone as USERNAME_FIELD
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []  # no other required fields

    objects = CustomerManager()

    def __str__(self):
        return self.get_full_name() or self.phone
