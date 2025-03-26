from django.shortcuts import render

# Create your views here.
# publications/views.py
from rest_framework import status, permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Gazette, Report
from .serializers import GazetteSerializer, ReportSerializer

class GazetteListView(APIView):
    """
    API endpoint for listing and creating gazettes.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        gazettes = Gazette.objects.all()
        serializer = GazetteSerializer(gazettes, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        # Only admins can create gazettes
        if request.user.role != 'admin':
            return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
            
        serializer = GazetteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GazetteDetailView(APIView):
    """
    API endpoint for retrieving, updating, and deleting gazettes.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, pk):
        gazette = get_object_or_404(Gazette, pk=pk)
        serializer = GazetteSerializer(gazette)
        return Response(serializer.data)
    
    def put(self, request, pk):
        # Only admins can update gazettes
        if request.user.role != 'admin':
            return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
            
        gazette = get_object_or_404(Gazette, pk=pk)
        serializer = GazetteSerializer(gazette, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        # Only admins can delete gazettes
        if request.user.role != 'admin':
            return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
            
        gazette = get_object_or_404(Gazette, pk=pk)
        gazette.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ReportListView(APIView):
    """
    API endpoint for listing and creating reports.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        reports = Report.objects.all()
        serializer = ReportSerializer(reports, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        # Only admins can create reports
        if request.user.role != 'admin':
            return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
            
        serializer = ReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReportDetailView(APIView):
    """
    API endpoint for retrieving, updating, and deleting reports.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, pk):
        report = get_object_or_404(Report, pk=pk)
        serializer = ReportSerializer(report)
        return Response(serializer.data)
    
    def put(self, request, pk):
        # Only admins can update reports
        if request.user.role != 'admin':
            return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
            
        report = get_object_or_404(Report, pk=pk)
        serializer = ReportSerializer(report, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        # Only admins can delete reports
        if request.user.role != 'admin':
            return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
            
        report = get_object_or_404(Report, pk=pk)
        report.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)