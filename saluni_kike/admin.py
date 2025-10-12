from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Salon, Service, Stylist, AvailabilitySlot, Booking, Payment, Review

# Use the custom user model dynamically for references only
Customer = get_user_model()  # Do NOT register Customer here

# ---------------------------
# Salon Admin
# ---------------------------
@admin.register(Salon)
class SalonAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'address',
        'region',
        'district',
        'street',
        'phone',
        'email',
        'website',
        'latitude',
        'longitude',
    )
    search_fields = (
        'name',
        'address',
        'region',
        'district',
        'street',
        'phone',
        'email',
    )
    list_filter = (
        'region',
        'district',
    )

# ---------------------------
# Service Admin
# ---------------------------
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'salon', 'price', 'duration_minutes')
    list_filter = ('salon',)

# ---------------------------
# Stylist Admin
# ---------------------------
@admin.register(Stylist)
class StylistAdmin(admin.ModelAdmin):
    list_display = ('name', 'salon', 'is_active')
    list_filter = ('salon', 'is_active')

# ---------------------------
# AvailabilitySlot Admin
# ---------------------------
@admin.register(AvailabilitySlot)
class AvailabilitySlotAdmin(admin.ModelAdmin):
    list_display = ('stylist', 'start', 'end', 'is_booked')
    list_filter = ('stylist', 'is_booked')

# ---------------------------
# Booking Admin
# ---------------------------
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('customer', 'salon', 'service', 'start_datetime', 'status')
    list_filter = ('status', 'salon')

# ---------------------------
# Payment Admin
# ---------------------------
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('booking', 'amount', 'method', 'status')
    list_filter = ('status', 'method')

# ---------------------------
# Review Admin
# ---------------------------
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('salon', 'customer', 'rating', 'created_at')
    list_filter = ('salon', 'rating')
