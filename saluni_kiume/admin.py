from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import MaleSalon, MaleService, MaleStylist, MaleAvailabilitySlot, MaleBooking, MalePayment, MaleReview

# Get the custom user model (for reference only)
Customer = get_user_model()  # You can still use Customer in ForeignKey fields

# Register models (do NOT register Customer again)
admin.site.register(MaleSalon)
admin.site.register(MaleService)
admin.site.register(MaleStylist)
admin.site.register(MaleAvailabilitySlot)
admin.site.register(MaleBooking)
admin.site.register(MalePayment)
admin.site.register(MaleReview)
