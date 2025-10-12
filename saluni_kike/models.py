# salon_app/models.py
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.utils import timezone

# -------------------
# Validators
# -------------------
PHONE_REGEX = RegexValidator(
    regex=r'^\+?[0-9]{9,15}$',
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
)

# -------------------
# Salon Model
# -------------------
class Salon(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=300)

    # Detailed location
    region = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    street = models.CharField(max_length=200)

    # GPS coordinates
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    phone = models.CharField(validators=[PHONE_REGEX], max_length=16, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    # Social media
    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)

    # JSON for opening hours
    opening_hours = models.JSONField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def average_rating(self):
        return self.reviews.aggregate(models.Avg('rating'))['rating__avg']

# -------------------
# Service Model
# -------------------
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

# -------------------
# Stylist Model
# -------------------
class Stylist(models.Model):
    salon = models.ForeignKey(Salon, related_name='stylists', on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    bio = models.TextField(blank=True)
    specialties = models.JSONField(blank=True, null=True, default=list)  # list of strings
    is_active = models.BooleanField(default=True)
    photo_url = models.URLField(blank=True, null=True)  # external image URL

    class Meta:
        ordering = ['salon', 'name']

    def __str__(self):
        return f"{self.name} ({self.salon.name})"

# -------------------
# Availability Slot
# -------------------
class AvailabilitySlot(models.Model):
    stylist = models.ForeignKey(Stylist, related_name='availability', on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()
    is_booked = models.BooleanField(default=False)

    class Meta:
        indexes = [models.Index(fields=['stylist', 'start'])]
        ordering = ['stylist', 'start']

    def clean(self):
        if self.start >= self.end:
            raise ValueError('Availability slot start must be before end')

    def __str__(self):
        return f"{self.stylist.name}: {self.start.isoformat()} -> {self.end.isoformat()}"

# -------------------
# Booking Model
# -------------------
class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No-show'),
    ]

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='bookings', on_delete=models.CASCADE)
    salon = models.ForeignKey(Salon, related_name='bookings', on_delete=models.CASCADE)
    service = models.ForeignKey(Service, related_name='bookings', on_delete=models.CASCADE)
    stylist = models.ForeignKey(Stylist, related_name='bookings', on_delete=models.SET_NULL, null=True, blank=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['salon', 'start_datetime']),
            models.Index(fields=['customer', 'start_datetime'])
        ]
        ordering = ['-start_datetime']

    def save(self, *args, **kwargs):
        # auto-calc end_datetime if missing
        if not self.end_datetime and self.service:
            self.end_datetime = self.start_datetime + timezone.timedelta(minutes=self.service.duration_minutes)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking #{self.pk} — {self.customer} @ {self.salon} on {self.start_datetime.isoformat()}"

# -------------------
# Payment Model
# -------------------
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

# -------------------
# Review Model
# -------------------
class Review(models.Model):
    booking = models.OneToOneField(Booking, related_name='review', on_delete=models.CASCADE)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviews', on_delete=models.CASCADE)
    salon = models.ForeignKey(Salon, related_name='reviews', on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.rating}⭐ — {self.salon.name} by {self.customer.username}"
