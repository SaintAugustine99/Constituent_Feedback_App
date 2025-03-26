# publications/serializers.py
from rest_framework import serializers
from .models import Gazette, Report
from feedback.serializers import CategorySerializer

class GazetteSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = Gazette
        fields = ['id', 'title', 'description', 'document_url', 'publish_date', 'category']

class ReportSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = Report
        fields = ['id', 'title', 'institution_name', 'report_year', 'document_url', 'category']