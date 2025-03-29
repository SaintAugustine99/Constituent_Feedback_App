# analytics/web_views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Count, Avg, F, Sum, Q
from django.utils import timezone
from datetime import timedelta
from accounts.models import User, District
from feedback.models import Feedback, Category
from complaints.models import Complaint
from publications.models import Gazette, Report

@login_required
def admin_dashboard(request):
    """View for the admin dashboard with summary statistics"""
    # Check if user is admin
    if request.user.role != 'admin':
        return HttpResponseForbidden("You don't have permission to access the admin dashboard.")
    
    # Calculate current date and date 30 days ago
    today = timezone.now().date()
    thirty_days_ago = today - timedelta(days=30)
    
    # Get counts of various entities
    user_stats = {
        'total_users': User.objects.filter(role='constituent').count(),
        'verified_users': User.objects.filter(is_verified=True, role='constituent').count(),
    }
    
    feedback_stats = {
        'total_feedback': Feedback.objects.count(),
        'feedback_last_30_days': Feedback.objects.filter(created_at__date__gte=thirty_days_ago).count(),
        'pending_feedback': Feedback.objects.filter(status='pending').count(),
        'resolved_feedback': Feedback.objects.filter(status='resolved').count(),
    }
    
    complaint_stats = {
        'total_complaints': Complaint.objects.count(),
        'complaints_last_30_days': Complaint.objects.filter(created_at__date__gte=thirty_days_ago).count(),
        'pending_complaints': Complaint.objects.filter(status='submitted').count(),
    }
    
    publication_stats = {
        'total_gazettes': Gazette.objects.count(),
        'total_reports': Report.objects.count(),
    }
    
    # Get feedback categorized by status
    status_distribution = dict(
        Feedback.objects.values('status')
        .annotate(count=Count('id'))
        .values_list('status', 'count')
    )
    
    # Get feedback categorized by category
    category_distribution = dict(
        Feedback.objects.values('category__name')
        .annotate(count=Count('id'))
        .values_list('category__name', 'count')
    )
    
    # Replace None key with "Uncategorized"
    if None in category_distribution:
        category_distribution["Uncategorized"] = category_distribution.pop(None)
    
    # Get district distribution
    district_feedback_counts = dict(
        User.objects.filter(feedback__isnull=False)
        .values('district__name')
        .annotate(count=Count('feedback'))
        .values_list('district__name', 'count')
    )
    
    # Replace None key with "No District"
    if None in district_feedback_counts:
        district_feedback_counts["No District"] = district_feedback_counts.pop(None)
    
    # Sentiment distribution
    sentiment_distribution = {
        'positive': Feedback.objects.filter(sentiment_score__gt=0.6).count(),
        'neutral': Feedback.objects.filter(sentiment_score__gte=0.4, sentiment_score__lte=0.6).count(),
        'negative': Feedback.objects.filter(sentiment_score__lt=0.4).count(),
    }
    
    # Dummy recent activity for example
    recent_activity = [
        {
            'user': {'first_name': 'John', 'last_name': 'Doe'},
            'action': 'submitted feedback',
            'item': 'Street Lighting Issue',
            'link': '#',
            'time_ago': '5 minutes ago'
        },
        {
            'user': {'first_name': 'Jane', 'last_name': 'Smith'},
            'action': 'filed complaint to',
            'item': 'Transport Commission',
            'link': '#',
            'time_ago': '2 hours ago'
        },
        {
            'user': {'first_name': 'Admin', 'last_name': 'User'},
            'action': 'published new gazette',
            'item': 'Q1 Budget Report',
            'link': '#',
            'time_ago': '1 day ago'
        }
    ]
    
    context = {
        'user_stats': user_stats,
        'feedback_stats': feedback_stats,
        'complaint_stats': complaint_stats,
        'publication_stats': publication_stats,
        'status_distribution': status_distribution,
        'category_distribution': category_distribution,
        'district_feedback_counts': district_feedback_counts,
        'sentiment_distribution': sentiment_distribution,
        'recent_activity': recent_activity,
    }
    
    return render(request, 'analytics/dashboard.html', context)

@login_required
def feedback_analytics(request):
    """View for detailed feedback analytics"""
    # Check if user is admin
    if request.user.role != 'admin':
        return HttpResponseForbidden("You don't have permission to access analytics.")
    
    # Implementation similar to admin_dashboard but with more detailed feedback stats
    # For brevity, we'll just redirect to the dashboard in this example
    return redirect('admin_dashboard')

@login_required
def geographic_analytics(request):
    """View for geographic analytics"""
    # Check if user is admin
    if request.user.role != 'admin':
        return HttpResponseForbidden("You don't have permission to access analytics.")
    
    # Implementation similar to admin_dashboard but with more detailed geographic stats
    # For brevity, we'll just redirect to the dashboard in this example
    return redirect('admin_dashboard')

@login_required
def sentiment_analytics(request):
    """View for sentiment analysis"""
    # Check if user is admin
    if request.user.role != 'admin':
        return HttpResponseForbidden("You don't have permission to access analytics.")
    
    # Implementation similar to admin_dashboard but with more detailed sentiment stats
    # For brevity, we'll just redirect to the dashboard in this example
    return redirect('admin_dashboard')

@login_required
def activity_log(request):
    """View for activity log"""
    # Check if user is admin
    if request.user.role != 'admin':
        return HttpResponseForbidden("You don't have permission to access the activity log.")
    
    # In a real implementation, you would retrieve actual activity log entries
    # For this example, we'll use dummy data
    
    # Dummy activity log for example
    activity_log = [
        {
            'user': {'first_name': 'John', 'last_name': 'Doe'},
            'action': 'submitted feedback',
            'item': 'Street Lighting Issue',
            'link': '#',
            'timestamp': timezone.now() - timedelta(minutes=5)
        },
        {
            'user': {'first_name': 'Jane', 'last_name': 'Smith'},
            'action': 'filed complaint to',
            'item': 'Transport Commission',
            'link': '#',
            'timestamp': timezone.now() - timedelta(hours=2)
        },
        {
            'user': {'first_name': 'Admin', 'last_name': 'User'},
            'action': 'published new gazette',
            'item': 'Q1 Budget Report',
            'link': '#',
            'timestamp': timezone.now() - timedelta(days=1)
        }
    ]
    
    context = {
        'activity_log': activity_log,
    }
    
    return render(request, 'analytics/activity_log.html', context)