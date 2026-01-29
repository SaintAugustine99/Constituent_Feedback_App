from django.contrib import admin
from .models import ServiceRequest


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'status', 'location_description', 'created_at', 'updated_at')
    list_filter = ('category', 'status')
    search_fields = ('description', 'location_description', 'user__username')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')
