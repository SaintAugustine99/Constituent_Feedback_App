# search/web_views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from feedback.models import Feedback
from publications.models import Gazette, Report
from complaints.models import Complaint

@login_required
def search_view(request):
    """View for searching across all content types"""
    query = request.GET.get('q', '')
    
    if not query:
        return render(request, 'search/results.html', {
            'query': query,
            'total_results': 0,
            'feedback_results': [],
            'complaint_results': [],
            'gazette_results': [],
            'report_results': [],
        })
    
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
        Q(title__icontains=query) | Q(description__icontains=query) | Q(commission_name__icontains=query)
    )
    if request.user.role != 'admin':
        complaint_results = complaint_results.filter(user=request.user)
    
    # Calculate total results
    total_results = (
        feedback_results.count() +
        gazette_results.count() +
        report_results.count() +
        complaint_results.count()
    )
    
    context = {
        'query': query,
        'total_results': total_results,
        'feedback_results': feedback_results,
        'complaint_results': complaint_results,
        'gazette_results': gazette_results,
        'report_results': report_results,
    }
    
    return render(request, 'search/results.html', context)