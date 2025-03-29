# feedback/web_urls.py
from django.urls import path
from . import web_views

urlpatterns = [
    path('', web_views.feedback_list, name='feedback_list'),
    path('<int:pk>/', web_views.feedback_detail, name='feedback_detail'),
    path('create/', web_views.feedback_create, name='create_feedback'),
    path('<int:pk>/edit/', web_views.feedback_edit, name='edit_feedback'),
    path('<int:feedback_id>/response/', web_views.add_response, name='add_response'),
    path('<int:feedback_id>/status/', web_views.update_feedback_status, name='update_feedback_status'),
    path('<int:feedback_id>/media/', web_views.upload_media, name='upload_media'),
]