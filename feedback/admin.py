from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Category, Feedback, Response, Media

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_category')
    search_fields = ('name',)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'status', 'created_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('title', 'description')

@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('feedback', 'responder', 'created_at', 'is_public')
    list_filter = ('is_public', 'created_at')
    search_fields = ('content',)

@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('feedback', 'file_type', 'created_at')
    list_filter = ('file_type', 'created_at')