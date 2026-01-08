from django.contrib import admin
from .models import Docket, InstrumentCategory, LegalInstrument, StatusReport, PublicFeedback

# 1. Customizing the Header (Personal Touch)
admin.site.site_header = "Kenya Public Participation Admin"
admin.site.site_title = "Participation Portal"
admin.site.index_title = "Welcome to the Legislative Tracker"

@admin.register(Docket)
class DocketAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'website_url')
    list_filter = ('level',)
    search_fields = ('name',)

@admin.register(LegalInstrument)
class InstrumentAdmin(admin.ModelAdmin):
    # This creates the "Dashboard" view for clerks
    list_display = ('title', 'docket', 'category', 'current_status', 'participation_deadline', 'is_open_display')
    list_filter = ('current_status', 'docket__level', 'category')
    search_fields = ('title', 'summary_text')
    date_hierarchy = 'created_at' # Drill down by date
    
    # Organize the data entry form nicely
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'docket', 'category')
        }),
        ('Documentation', {
            'fields': ('legal_text_url', 'summary_text')
        }),
        ('Public Participation Timeline', {
            'fields': ('published_date', 'participation_deadline', 'current_status'),
            'description': 'Ensure the deadline allows for "Reasonable Time" as per Supreme Court guidelines.'
        }),
    )

    def is_open_display(self, obj):
        return obj.is_open()
    is_open_display.boolean = True
    is_open_display.short_description = "Active?"

@admin.register(PublicFeedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'instrument', 'position', 'submitted_at', 'has_evidence')
    list_filter = ('position', 'instrument', 'submitted_at')
    readonly_fields = ('submitted_at',) # Prevent tampering with dates

    def has_evidence(self, obj):
        return bool(obj.image_evidence)
    has_evidence.boolean = True

# Register standard models normally
admin.site.register(InstrumentCategory)
admin.site.register(StatusReport)
