# feedback/urls.py
from django.urls import path
from .views import (
    CategoryListView,
    FeedbackListCreateView,
    FeedbackDetailView,
    ResponseCreateView,
     MediaDeleteView,
     MediaUploadView,
)

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('feedback/', FeedbackListCreateView.as_view(), name='feedback-list-create'),
    path('feedback/<int:pk>/', FeedbackDetailView.as_view(), name='feedback-detail'),
    path('feedback/<int:feedback_id>/responses/', ResponseCreateView.as_view(), name='response-create'),
    path('feedback/<int:feedback_id>/media/', MediaUploadView.as_view(), name='media-upload'),
    path('media/<int:media_id>/', MediaDeleteView.as_view(), name='media-delete'),
]