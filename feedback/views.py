from django.shortcuts import render

# Create your views here.
# feedback/views.py
from rest_framework import status, permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Category, Feedback, Response as FeedbackResponse, Media
from .serializers import (
    CategorySerializer, 
    FeedbackSerializer, 
    FeedbackCreateSerializer,
    ResponseSerializer, 
    MediaSerializer
)

class CategoryListView(generics.ListAPIView):
    """
    API endpoint to list all categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class FeedbackListCreateView(APIView):
    """
    API endpoint for listing and creating feedback.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        # For regular users, show only their feedback
        if request.user.role != 'admin':
            feedback = Feedback.objects.filter(user=request.user)
        else:
            # Admins can see all feedback
            feedback = Feedback.objects.all()
            
        serializer = FeedbackSerializer(feedback, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = FeedbackCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            # Return the complete feedback object
            feedback = Feedback.objects.get(id=serializer.instance.id)
            return Response(FeedbackSerializer(feedback).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FeedbackDetailView(APIView):
    """
    API endpoint for retrieving, updating, and deleting feedback.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self, pk, user):
        feedback = get_object_or_404(Feedback, pk=pk)
        # Check if user has permission
        if user.role != 'admin' and feedback.user != user:
            raise permissions.PermissionDenied
        return feedback
    
    def get(self, request, pk):
        feedback = self.get_object(pk, request.user)
        serializer = FeedbackSerializer(feedback)
        return Response(serializer.data)
    
    def put(self, request, pk):
        feedback = self.get_object(pk, request.user)
        serializer = FeedbackCreateSerializer(feedback, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(FeedbackSerializer(feedback).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        feedback = self.get_object(pk, request.user)
        feedback.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ResponseCreateView(APIView):
    """
    API endpoint for creating responses to feedback.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, feedback_id):
        # Only admins can respond
        if request.user.role != 'admin':
            return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
            
        feedback = get_object_or_404(Feedback, pk=feedback_id)
        
        serializer = ResponseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(feedback=feedback, responder=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)