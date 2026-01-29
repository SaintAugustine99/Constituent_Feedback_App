from rest_framework import generics, permissions, filters
from .models import Facility, Booking
from .serializers import FacilitySerializer, BookingSerializer
from django_filters.rest_framework import DjangoFilterBackend

class FacilityList(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['ward', 'facility_type']
    search_fields = ['name', 'description']

class BookingListCreate(generics.ListCreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users see their own bookings
        return Booking.objects.filter(user=self.request.user).order_by('-start_time')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
