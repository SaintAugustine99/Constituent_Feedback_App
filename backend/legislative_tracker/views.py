from django.db.models import Count, Q
from rest_framework import viewsets, filters, status, permissions
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
    permission_classes = [permissions.AllowAny]
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

    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """Returns feedback statistics for a specific instrument"""
        instrument = self.get_object()
        feedback = instrument.feedback.all()
        total = feedback.count()
        positions = feedback.values('position').annotate(count=Count('id'))
        position_counts = {p['position']: p['count'] for p in positions}
        return Response({
            'instrument_id': instrument.id,
            'instrument_title': instrument.title,
            'total_feedback': total,
            'positions': {
                'SUPPORT': position_counts.get('SUPPORT', 0),
                'OPPOSE': position_counts.get('OPPOSE', 0),
                'AMEND': position_counts.get('AMEND', 0),
            }
        })


class FeedbackViewSet(viewsets.ModelViewSet):
    """
    Handles posting feedback with images.
    AllowAny for list/create so guests can submit feedback.
    Admin-only for update/delete.
    """
    queryset = PublicFeedback.objects.all()
    serializer_class = PublicFeedbackSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        extra = {'user': user}
        if user and hasattr(user, 'ward') and user.ward:
            extra['ward_ref'] = user.ward
            extra['constituency_ref'] = user.ward.constituency
        serializer.save(**extra)


class DocketViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Docket.objects.all()
    serializer_class = DocketSerializer
