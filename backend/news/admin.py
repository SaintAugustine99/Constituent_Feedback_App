from django.contrib import admin
from .models import GovernmentResource, NewsArticle


@admin.register(GovernmentResource)
class GovernmentResourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'order']
    list_filter = ['category']
    list_editable = ['order']


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'source_name', 'published_at']
    list_filter = ['source_name']
    search_fields = ['title', 'description']
