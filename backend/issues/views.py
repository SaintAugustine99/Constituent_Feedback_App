from rest_framework import generics, permissions, parsers
from .models import ServiceRequest
from .serializers import ServiceRequestSerializer

class ServiceRequestListCreate(generics.ListCreateAPIView):
    serializer_class = ServiceRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser] # To handle image uploads

    def get_queryset(self):
        # Users see only their own requests
        return ServiceRequest.objects.filter(user=self.request.user).order_by('-created_at')
