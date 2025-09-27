from django.contrib import admin
from .models import Customer, Salon, Service, Stylist, AvailabilitySlot, Booking, Payment, Review

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'phone')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'salon', 'price', 'duration_minutes')
    list_filter = ('salon',)

@admin.register(Stylist)
class StylistAdmin(admin.ModelAdmin):
    list_display = ('name', 'salon', 'is_active')
    list_filter = ('salon', 'is_active')

@admin.register(AvailabilitySlot)
class AvailabilitySlotAdmin(admin.ModelAdmin):
    list_display = ('stylist', 'start', 'end', 'is_booked')
    list_filter = ('stylist', 'is_booked')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('customer', 'salon', 'service', 'start_datetime', 'status')
    list_filter = ('status', 'salon')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('booking', 'amount', 'method', 'status')
    list_filter = ('status', 'method')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('salon', 'customer', 'rating', 'created_at')
    list_filter = ('salon', 'rating')

from django.contrib import admin
from .models import Salon

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

