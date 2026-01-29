from rest_framework import serializers
from .models import Docket, LegalInstrument, StatusReport, PublicFeedback, InstrumentCategory

class DocketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Docket
        fields = '__all__'

class StatusReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusReport
        fields = ['id', 'title', 'content', 'report_date', 'attachment']

class LegalInstrumentListSerializer(serializers.ModelSerializer):
    """Lighter serializer for list views (landing page)"""
    docket_name = serializers.CharField(source='docket.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    is_active = serializers.BooleanField(source='is_open', read_only=True)

    class Meta:
        model = LegalInstrument
        fields = ['id', 'title', 'docket_name', 'category_name', 'participation_deadline', 'current_status', 'is_active']

class LegalInstrumentDetailSerializer(serializers.ModelSerializer):
    """Detailed view including status history"""
    docket = DocketSerializer()
    status_reports = StatusReportSerializer(many=True, read_only=True)
    
    class Meta:
        model = LegalInstrument
        fields = '__all__'

class PublicFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicFeedback
        fields = '__all__'
        read_only_fields = ['submitted_at', 'is_verified', 'user', 'constituency_ref', 'ward_ref']
