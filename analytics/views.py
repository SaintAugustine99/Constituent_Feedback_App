from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Avg, F, Sum, Q
from django.utils import timezone
from datetime import timedelta
from accounts.models import User, District
from feedback.models import Feedback, Category
from complaints.models import Complaint
from publications.models import Gazette, Report

class AdminDashboardView(APIView):
    """
    API endpoint providing summary statistics for admin dashboard.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        # Check if user is admin
        if request.user.role != 'admin':
            return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
        
        # Calculate current date and date 30 days ago
        today = timezone.now().date()
        thirty_days_ago = today - timedelta(days=30)
        
        # Get counts of various entities
        user_count = User.objects.filter(role='constituent').count()
        feedback_count = Feedback.objects.count()
        feedback_last_30_days = Feedback.objects.filter(created_at__date__gte=thirty_days_ago).count()
        pending_feedback = Feedback.objects.filter(status='pending').count()
        resolved_feedback = Feedback.objects.filter(status='resolved').count()
        
        complaint_count = Complaint.objects.count()
        complaint_last_30_days = Complaint.objects.filter(created_at__date__gte=thirty_days_ago).count()
        pending_complaints = Complaint.objects.filter(status='submitted').count()
        
        # Prepare response data
        data = {
            'user_stats': {
                'total_users': user_count,
                'verified_users': User.objects.filter(is_verified=True, role='constituent').count(),
            },
            'feedback_stats': {
                'total_feedback': feedback_count,
                'feedback_last_30_days': feedback_last_30_days,
                'pending_feedback': pending_feedback,
                'resolved_feedback': resolved_feedback,
            },
            'complaint_stats': {
                'total_complaints': complaint_count,
                'complaints_last_30_days': complaint_last_30_days,
                'pending_complaints': pending_complaints,
            },
            'publication_stats': {
                'total_gazettes': Gazette.objects.count(),
                'total_reports': Report.objects.count(),
            }
        }
        
        return Response(data)

class FeedbackAnalyticsView(APIView):
    """
    API endpoint providing detailed analytics on feedback data.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        # Check if user is admin
        if request.user.role != 'admin':
            return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
        
        # Get feedback categorized by status
        status_counts = Feedback.objects.values('status').annotate(count=Count('id')).order_by('status')
        
        # Get feedback categorized by category
        category_counts = Feedback.objects.values(
            'category__name'
        ).annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Get feedback trends over time (by month)
        # This requires more advanced Django ORM techniques or raw SQL
        # For now, we'll use a simplified approach
        
        # Prepare response data
        data = {
            'status_distribution': {item['status']: item['count'] for item in status_counts},
            'category_distribution': {item['category__name'] or 'Uncategorized': item['count'] for item in category_counts},
            # You could add more analytics here
        }
        
        return Response(data)

class UserAnalyticsView(APIView):
    """
    API endpoint providing detailed analytics on user activity.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        # Check if user is admin
        if request.user.role != 'admin':
            return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
        
        # Get counts of users by district
        district_counts = User.objects.values(
            'district__name'
        ).annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Get most active users (by feedback count)
        active_users = User.objects.annotate(
            feedback_count=Count('feedback')
        ).values(
            'id', 'email', 'first_name', 'last_name', 'feedback_count'
        ).order_by('-feedback_count')[:10]  # Top 10
        
        # Prepare response data
        data = {
            'district_distribution': {item['district__name'] or 'No District': item['count'] for item in district_counts},
            'most_active_users': list(active_users),
            # You could add more user analytics here
        }
        
        return Response(data)

class GeographicAnalyticsView(APIView):
    """
    API endpoint providing geographic distribution of feedback.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        # Check if user is admin
        if request.user.role != 'admin':
            return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
        
        # Get feedback with location data
        feedback_with_location = Feedback.objects.exclude(location_data=None)
        
        # Count feedback by district
        district_counts = User.objects.filter(
            feedback__isnull=False
        ).values(
            'district__name'
        ).annotate(
            count=Count('feedback')
        ).order_by('-count')
        
        # Prepare response data
        data = {
            'district_feedback_counts': {item['district__name'] or 'No District': item['count'] for item in district_counts},
            'feedback_with_location_count': feedback_with_location.count(),
            # We could add more geographic analytics here
        }
        
        return Response(data)

class SentimentAnalysisView(APIView):
    """
    API endpoint providing sentiment analysis of feedback.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        # Check if user is admin
        if request.user.role != 'admin':
            return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
        
        # Get average sentiment score
        avg_sentiment = Feedback.objects.exclude(sentiment_score=None).aggregate(Avg('sentiment_score'))
        
        # Get feedback with highest and lowest sentiment
        highest_sentiment = Feedback.objects.exclude(sentiment_score=None).order_by('-sentiment_score')[:5]
        lowest_sentiment = Feedback.objects.exclude(sentiment_score=None).order_by('sentiment_score')[:5]
        
        # Get sentiment distribution (example: count of positive, neutral, negative)
        positive_count = Feedback.objects.filter(sentiment_score__gt=0.5).count()
        neutral_count = Feedback.objects.filter(sentiment_score__gte=0.3, sentiment_score__lte=0.7).count()
        negative_count = Feedback.objects.filter(sentiment_score__lt=0.3).count()
        
        # Prepare response data
        data = {
            'average_sentiment': avg_sentiment['sentiment_score__avg'],
            'highest_sentiment': [
                {'id': f.id, 'title': f.title, 'score': f.sentiment_score} 
                for f in highest_sentiment
            ],
            'lowest_sentiment': [
                {'id': f.id, 'title': f.title, 'score': f.sentiment_score} 
                for f in lowest_sentiment
            ],
            'sentiment_distribution': {
                'positive': positive_count,
                'neutral': neutral_count,
                'negative': negative_count
            }
        }
        
        return Response(data)