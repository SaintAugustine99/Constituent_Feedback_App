# In feedback_platform/views.py
from django.shortcuts import render
from django.db.models import Count
from feedback.models import Feedback
from complaints.models import Complaint
from publications.models import Gazette, Report
from accounts.models import User
from django.utils import timezone
from datetime import timedelta

def home_view(request):
    """View for rendering the home page with summary statistics and recent content"""
    # Calculate current date and date 30 days ago
    today = timezone.now().date()
    thirty_days_ago = today - timedelta(days=30)
    
    # Basic statistics
    stats = {
        'user_count': User.objects.filter(role='constituent').count(),
        'feedback_count': Feedback.objects.count(),
        'complaint_count': Complaint.objects.count(),
        'resolved_count': Feedback.objects.filter(status='resolved').count() + 
                         Complaint.objects.filter(status='resolved').count(),
    }
    
    # Recent public feedback
    recent_feedback = Feedback.objects.filter(is_public=True).order_by('-created_at')[:4]
    
    # Process status fields to replace underscores with spaces
    for feedback in recent_feedback:
        feedback.status_display = feedback.status.replace('_', ' ').title()
    
    # Recent publications (both gazettes and reports)
    recent_gazettes = Gazette.objects.all().order_by('-publish_date')[:3]
    recent_reports = Report.objects.all().order_by('-report_year')[:3]
    
    # Combine and sort by date
    recent_publications = list(recent_gazettes) + list(recent_reports)
    # Use a simpler approach to sort publications that works with different date fields
    recent_publications = sorted(
        recent_publications, 
        key=lambda x: getattr(x, 'publish_date', timezone.now().date()),
        reverse=True
    )[:6]
    
    context = {
        'stats': stats,
        'recent_feedback': recent_feedback,
        'recent_publications': recent_publications,
    }
    
    return render(request, 'home.html', context)