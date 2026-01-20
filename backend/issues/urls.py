from django.urls import path
from .views import ServiceRequestListCreate

urlpatterns = [
    path('requests/', ServiceRequestListCreate.as_view(), name='service-requests'),
]
