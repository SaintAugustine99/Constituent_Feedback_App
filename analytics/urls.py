# analytics/urls.py
from django.urls import path
from .views import (
    AdminDashboardView,
    FeedbackAnalyticsView,
    UserAnalyticsView,
    GeographicAnalyticsView,
    SentimentAnalysisView
)

urlpatterns = [
    path('dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),
    path('feedback-analytics/', FeedbackAnalyticsView.as_view(), name='feedback-analytics'),
    path('user-analytics/', UserAnalyticsView.as_view(), name='user-analytics'),
    path('geographic-analytics/', GeographicAnalyticsView.as_view(), name='geographic-analytics'),
    path('sentiment-analysis/', SentimentAnalysisView.as_view(), name='sentiment-analysis'),
]