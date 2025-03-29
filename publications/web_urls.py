# publications/web_urls.py
from django.urls import path
from . import web_views

urlpatterns = [
    path('gazettes/', web_views.gazette_list, name='gazette_list'),
    path('gazettes/<int:pk>/', web_views.gazette_detail, name='gazette_detail'),
    path('gazettes/create/', web_views.gazette_create, name='create_gazette'),
    path('gazettes/<int:pk>/edit/', web_views.gazette_edit, name='edit_gazette'),
    
    path('reports/', web_views.report_list, name='report_list'),
    path('reports/<int:pk>/', web_views.report_detail, name='report_detail'),
    path('reports/create/', web_views.report_create, name='create_report'),
    path('reports/<int:pk>/edit/', web_views.report_edit, name='edit_report'),
]