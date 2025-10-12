from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(UserAdmin):
    model = Customer

    # Replace username references with phone
    list_display = ('phone', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    ordering = ('phone',)
    search_fields = ('phone', 'email')

    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'role', 'profile_image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2', 'role', 'is_active', 'is_staff')}
        ),
    )
