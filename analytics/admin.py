from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import SentimentAnalysisResult

@admin.register(SentimentAnalysisResult)
class SentimentAnalysisResultAdmin(admin.ModelAdmin):
    list_display = ('feedback', 'sentiment_score', 'processed_at')