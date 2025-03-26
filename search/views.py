from django.shortcuts import render

# Create your views here.
# search/views.py
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from feedback.models import Feedback
from publications.models import Gazette, Report
from complaints.models import Complaint
from feedback.serializers import FeedbackSerializer
from publications.serializers import GazetteSerializer, ReportSerializer
from complaints.serializers import ComplaintSerializer

class SearchView(APIView):
    """
    API endpoint for searching across all content types.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        query = request.query_params.get('q', '')
        if not query:
            return Response({"detail": "Search query is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Search in feedback
        feedback_results = Feedback.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
        if request.user.role != 'admin':
            feedback_results = feedback_results.filter(
                Q(user=request.user) | Q(is_public=True)
            )
        
        # Search in gazettes
        gazette_results = Gazette.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
        
        # Search in reports
        report_results = Report.objects.filter(
            Q(title__icontains=query) | Q(institution_name__icontains=query)
        )
        
        # Search in complaints
        complaint_results = Complaint.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
        if request.user.role != 'admin':
            complaint_results = complaint_results.filter(user=request.user)
        
        results = {
            'feedback': FeedbackSerializer(feedback_results, many=True).data,
            'gazettes': GazetteSerializer(gazette_results, many=True).data,
            'reports': ReportSerializer(report_results, many=True).data,
            'complaints': ComplaintSerializer(complaint_results, many=True).data,
        }
        
        return Response(results)