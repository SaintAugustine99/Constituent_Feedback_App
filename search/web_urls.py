# search/web_urls.py
from django.urls import path
from . import web_views

urlpatterns = [
    path('', web_views.search_view, name='search'),
]