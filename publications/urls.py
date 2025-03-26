# publications/urls.py
from django.urls import path
from .views import (
    GazetteListView,
    GazetteDetailView,
    ReportListView,
    ReportDetailView
)

urlpatterns = [
    path('gazettes/', GazetteListView.as_view(), name='gazette-list'),
    path('gazettes/<int:pk>/', GazetteDetailView.as_view(), name='gazette-detail'),
    path('reports/', ReportListView.as_view(), name='report-list'),
    path('reports/<int:pk>/', ReportDetailView.as_view(), name='report-detail'),
]