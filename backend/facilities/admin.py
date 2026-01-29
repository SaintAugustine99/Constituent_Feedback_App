from django.contrib import admin
from .models import Facility, Booking


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'facility_type', 'ward', 'capacity', 'price_per_hour')
    list_filter = ('facility_type', 'ward__constituency__county')
    search_fields = ('name', 'description', 'ward__name')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'facility', 'start_time', 'end_time', 'status', 'created_at')
    list_filter = ('status', 'facility')
    search_fields = ('user__username', 'facility__name', 'purpose')
    date_hierarchy = 'start_time'
