from django.contrib import admin
from .models import Project, ProjectUpdate


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'ward', 'status', 'budget_allocated', 'amount_spent', 'completion_percentage', 'contractor_name')
    list_filter = ('status', 'ward__constituency__county')
    search_fields = ('name', 'contractor_name', 'description')
    date_hierarchy = 'start_date'


@admin.register(ProjectUpdate)
class ProjectUpdateAdmin(admin.ModelAdmin):
    list_display = ('project', 'user', 'verified', 'created_at')
    list_filter = ('verified', 'project')
    search_fields = ('comment', 'user__username', 'project__name')
    date_hierarchy = 'created_at'
