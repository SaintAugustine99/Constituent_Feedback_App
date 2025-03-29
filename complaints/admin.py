from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Complaint, ComplaintUpdate, ComplaintDocument

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('title', 'commission_name', 'user', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'description', 'commission_name')

@admin.register(ComplaintUpdate)
class ComplaintUpdateAdmin(admin.ModelAdmin):
    list_display = ('complaint', 'user', 'is_official', 'created_at')
    list_filter = ('is_official', 'created_at')

@admin.register(ComplaintDocument)
class ComplaintDocumentAdmin(admin.ModelAdmin):
    list_display = ('complaint', 'uploaded_at')