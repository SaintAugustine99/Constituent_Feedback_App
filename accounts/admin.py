from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import User, District

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'district', 'is_verified')
    list_filter = ('role', 'is_verified', 'district')
    search_fields = ('email', 'first_name', 'last_name')

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name',)