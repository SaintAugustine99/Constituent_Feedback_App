from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import LegalInstrument, PublicFeedback, Docket
from .serializers import (
    LegalInstrumentListSerializer, 
    LegalInstrumentDetailSerializer, 
    PublicFeedbackSerializer,
    DocketSerializer
)

class LegalInstrumentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only view for constituents to browse Bills/Policies.
    Supports filtering by Docket (e.g. show only Nairobi County bills).
    """
    queryset = LegalInstrument.objects.all().order_by('-created_at')
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'docket__name', 'summary_text']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return LegalInstrumentDetailSerializer
        return LegalInstrumentListSerializer

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Custom endpoint to get ONLY items currently open for participation"""
        active_instruments = [i for i in self.queryset if i.is_open()]
        page = self.paginate_queryset(active_instruments)
        if page is not None:
             serializer = LegalInstrumentListSerializer(page, many=True)
             return self.get_paginated_response(serializer.data)
        serializer = LegalInstrumentListSerializer(active_instruments, many=True)
        return Response(serializer.data)

class FeedbackViewSet(viewsets.ModelViewSet):
    """
    Handles posting feedback with images.
    """
    queryset = PublicFeedback.objects.all()
    serializer_class = PublicFeedbackSerializer
    parser_classes = (MultiPartParser, FormParser) # Crucial for Image Uploads

    def create(self, request, *args, **kwargs):
        # Custom logic can go here (e.g., sending an email confirmation)
        return super().create(request, *args, **kwargs)

class DocketViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Docket.objects.all()
    serializer_class = DocketSerializer
