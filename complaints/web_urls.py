# complaints/web_urls.py
from django.urls import path
from . import web_views

urlpatterns = [
    path('', web_views.complaint_list, name='complaint_list'),
    path('<int:pk>/', web_views.complaint_detail, name='complaint_detail'),
    path('create/', web_views.complaint_create, name='create_complaint'),
    path('<int:pk>/edit/', web_views.complaint_edit, name='edit_complaint'),
    path('<int:pk>/status/', web_views.update_complaint_status, name='update_complaint_status'),
]