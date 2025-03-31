# complaints/urls.py
from django.urls import path
from .views import ComplaintListCreateView, ComplaintDetailView, ComplaintStatusUpdateView
from . import web_views

urlpatterns = [
    path('complaints/', ComplaintListCreateView.as_view(), name='complaint-list-create'),
    path('complaints/<int:pk>/', ComplaintDetailView.as_view(), name='complaint-detail'),
    path('complaints/<int:pk>/status/', ComplaintStatusUpdateView.as_view(), name='complaint-status-update'),
    path('<int:complaint_id>/update/', web_views.add_complaint_update, name='add_complaint_update'),
]