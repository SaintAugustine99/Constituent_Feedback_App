from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Gazette, Report

@admin.register(Gazette)
class GazetteAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish_date', 'category')
    list_filter = ('publish_date', 'category')
    search_fields = ('title', 'description')

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'institution_name', 'report_year', 'category')
    list_filter = ('report_year', 'category')
    search_fields = ('title', 'institution_name')