# analytics/web_urls.py
from django.urls import path
from . import web_views

urlpatterns = [
    path('dashboard/', web_views.admin_dashboard, name='admin_dashboard'),
    path('feedback/', web_views.feedback_analytics, name='feedback_analytics'),
    path('geographic/', web_views.geographic_analytics, name='geographic_analytics'),
    path('sentiment/', web_views.sentiment_analytics, name='sentiment_analytics'),
    path('activity-log/', web_views.activity_log, name='activity_log'),
]