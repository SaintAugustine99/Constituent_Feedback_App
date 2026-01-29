from django.contrib import admin
from .models import County, Constituency, Ward, Official

@admin.register(County)
class CountyAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')
    ordering = ('name',)

@admin.register(Constituency)
class ConstituencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'county')
    search_fields = ('name', 'county__name')
    list_filter = ('county',)
    autocomplete_fields = ['county'] # Requires CountyAdmin to have search_fields

@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
    list_display = ('name', 'constituency', 'get_county')
    search_fields = ('name', 'constituency__name')
    list_filter = ('constituency__county',)
    autocomplete_fields = ['constituency'] # Requires ConstituencyAdmin to have search_fields
    
    def get_county(self, obj):
        return obj.constituency.county.name
    get_county.short_description = 'County'
    get_county.admin_order_field = 'constituency__county'

@admin.register(Official)
class OfficialAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'ward', 'constituency', 'county', 'phone', 'email')
    list_filter = ('title', 'county')
    search_fields = ('name', 'email', 'phone')
    autocomplete_fields = ['ward', 'constituency', 'county']
