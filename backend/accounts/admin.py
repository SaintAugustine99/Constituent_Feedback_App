from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone_number', 'ward', 'is_verified')
    
    # Enable autocomplete for the ward field (requires WardAdmin to have search_fields)
    autocomplete_fields = ['ward']

    # Add custom fields to the edit form
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone_number', 'ward', 'is_verified')}),
    )
    
    # Add custom fields to the creation form
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('phone_number', 'ward', 'is_verified')}),
    )
