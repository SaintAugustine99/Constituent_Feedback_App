from django.urls import path
from .views import FacilityList, BookingListCreate

urlpatterns = [
    path('list/', FacilityList.as_view(), name='facility-list'),
    path('bookings/', BookingListCreate.as_view(), name='booking-list-create'),
]
