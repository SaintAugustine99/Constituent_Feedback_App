# complaints/urls.py
from django.urls import path
from .views import ComplaintListCreateView, ComplaintDetailView, ComplaintStatusUpdateView

urlpatterns = [
    path('complaints/', ComplaintListCreateView.as_view(), name='complaint-list-create'),
    path('complaints/<int:pk>/', ComplaintDetailView.as_view(), name='complaint-detail'),
    path('complaints/<int:pk>/status/', ComplaintStatusUpdateView.as_view(), name='complaint-status-update'),
]