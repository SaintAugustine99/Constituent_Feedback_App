from django.shortcuts import render

# Create your views here.
# complaints/views.py
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Complaint
from .serializers import ComplaintSerializer, ComplaintCreateSerializer

class ComplaintListCreateView(APIView):
    """
    API endpoint for listing and creating complaints.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        # For regular users, show only their complaints
        if request.user.role != 'admin':
            complaints = Complaint.objects.filter(user=request.user)
        else:
            # Admins can see all complaints
            complaints = Complaint.objects.all()
            
        serializer = ComplaintSerializer(complaints, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ComplaintCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            # Return the complete complaint object
            complaint = Complaint.objects.get(id=serializer.instance.id)
            return Response(ComplaintSerializer(complaint).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ComplaintDetailView(APIView):
    """
    API endpoint for retrieving, updating, and deleting complaints.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self, pk, user):
        complaint = get_object_or_404(Complaint, pk=pk)
        # Check if user has permission
        if user.role != 'admin' and complaint.user != user:
            raise permissions.PermissionDenied
        return complaint
    
    def get(self, request, pk):
        complaint = self.get_object(pk, request.user)
        serializer = ComplaintSerializer(complaint)
        return Response(serializer.data)
    
    def put(self, request, pk):
        complaint = self.get_object(pk, request.user)
        
        # Only admins can update status
        if 'status' in request.data and request.user.role != 'admin':
            return Response({"detail": "Not authorized to change status"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ComplaintCreateSerializer(complaint, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(ComplaintSerializer(complaint).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        complaint = self.get_object(pk, request.user)
        complaint.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ComplaintStatusUpdateView(APIView):
    """
    API endpoint for updating the status of a complaint (admin only).
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def put(self, request, pk):
        # Only admins can update status
        if request.user.role != 'admin':
            return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
            
        complaint = get_object_or_404(Complaint, pk=pk)
        
        if 'status' not in request.data:
            return Response({"detail": "Status field is required"}, status=status.HTTP_400_BAD_REQUEST)
            
        complaint.status = request.data['status']
        complaint.save()
        
        return Response(ComplaintSerializer(complaint).data)
