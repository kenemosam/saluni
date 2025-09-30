from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, RegexValidator, MaxValueValidator
from django.utils import timezone

PHONE_REGEX = RegexValidator(
    regex=r'^\+?[0-9]{9,15}$',
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
)


class Customer(AbstractUser):
    """Custom user model for customers (and optionally salon staff if you like).
    Uses Django's AbstractUser so you have username, email, password, first_name, last_name, etc.
    """
    phone = models.CharField(validators=[PHONE_REGEX], max_length=16, blank=True, null=True)
    is_phone_verified = models.BooleanField(default=False)
    # Add preferences, profile image, default payment method token, etc.
    profile_image = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.get_full_name() or self.username


from django.db import models
from django.core.validators import RegexValidator


class Salon(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=300)

    # New fields for detailed location
    region = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    street = models.CharField(max_length=200)

    # GPS coordinates
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    phone = models.CharField(validators=[PHONE_REGEX], max_length=16, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    # Social media links
    facebook = models.URLField(blank=True, null=True)   # Facebook link
    instagram = models.URLField(blank=True, null=True)  # Instagram link

    # opening_hours can be a JSON object like {"mon":["09:00","18:00"], ...}
    opening_hours = models.JSONField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def average_rating(self):
        return self.reviews.aggregate(models.Avg('rating'))['rating__avg']



class Service(models.Model):
    salon = models.ForeignKey(Salon, related_name='services', on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    duration_minutes = models.PositiveIntegerField(default=30)
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('salon', 'name')
        ordering = ['salon', 'name']

    def __str__(self):
        return f"{self.name} — {self.salon.name}"


from django.db import models

class Stylist(models.Model):
    salon = models.ForeignKey(Salon, related_name='stylists', on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    bio = models.TextField(blank=True)
    specialties = models.JSONField(blank=True, null=True, default=list)  # store as list of strings
    is_active = models.BooleanField(default=True)
    photo_url = models.URLField(blank=True, null=True)  # external image URL

    class Meta:
        ordering = ['salon', 'name']

    def __str__(self):
        return f"{self.name} ({self.salon.name})"




class AvailabilitySlot(models.Model):
    """Represents a time slot a stylist is available. You can create slots daily/weekly or dynamically.
    For larger scale, consider using a more efficient calendar/booking library.
    """
    stylist = models.ForeignKey(Stylist, related_name='availability', on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()
    is_booked = models.BooleanField(default=False)

    class Meta:
        indexes = [models.Index(fields=['stylist', 'start'])]
        ordering = ['stylist', 'start']

    def clean(self):
        # ensure start < end
        if self.start >= self.end:
            raise ValueError('Availability slot start must be before end')

    def __str__(self):
        return f"{self.stylist.name}: {self.start.isoformat()} -> {self.end.isoformat()}"


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No-show'),
    ]

    customer = models.ForeignKey(Customer, related_name='bookings', on_delete=models.CASCADE)
    salon = models.ForeignKey(Salon, related_name='bookings', on_delete=models.CASCADE)
    service = models.ForeignKey(Service, related_name='bookings', on_delete=models.CASCADE)
    stylist = models.ForeignKey(Stylist, related_name='bookings', on_delete=models.SET_NULL, null=True, blank=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)

    class Meta:
        indexes = [models.Index(fields=['salon', 'start_datetime']), models.Index(fields=['customer', 'start_datetime'])]
        ordering = ['-start_datetime']

    def save(self, *args, **kwargs):
        # auto-calc end_datetime if missing using service.duration_minutes
        if not self.end_datetime and self.service:
            self.end_datetime = self.start_datetime + timezone.timedelta(minutes=self.service.duration_minutes)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking #{self.pk} — {self.customer} @ {self.salon} on {self.start_datetime.isoformat()}"


class Payment(models.Model):
    METHOD_CHOICES = [
        ('mpesa', 'M-Pesa'),
        ('tigo_pesa', 'Tigo Pesa'),
        ('card', 'Card'),
        ('cash', 'Cash'),
    ]
    STATUS_CHOICES = [
        ('initiated', 'Initiated'),
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    booking = models.OneToOneField(Booking, related_name='payment', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    method = models.CharField(max_length=30, choices=METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='initiated')
    transaction_id = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.amount} ({self.get_status_display()}) for Booking {self.booking_id}"


class Review(models.Model):
    booking = models.OneToOneField(Booking, related_name='review', on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, related_name='reviews', on_delete=models.CASCADE)
    salon = models.ForeignKey(Salon, related_name='reviews', on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.rating}⭐ — {self.salon.name} by {self.customer.username}"


# saluni_kike/forms.py
from django import forms
from .models import Salon

class SalonQuickForm(forms.ModelForm):
    class Meta:
        model = Salon
        fields = ['name', 'phone']  # field chache tu
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Jina la saluni'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Namba ya simu'}),
        }
