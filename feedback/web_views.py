# feedback/web_views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Feedback, Category, Response as FeedbackResponse, Media
from .forms import FeedbackForm, ResponseForm, MediaForm  # You'll need to create these forms

@login_required
def feedback_list(request):
    """View to display a list of feedback"""
    # Get filter parameters
    category_id = request.GET.get('category')
    status = request.GET.get('status')
    
    # Base queryset
    if request.user.role == 'admin':
        feedback_queryset = Feedback.objects.all()
    else:
        # For regular users, show their own feedback and public feedback
        feedback_queryset = Feedback.objects.filter(
            models.Q(user=request.user) | models.Q(is_public=True)
        )
    
    # Apply filters
    if category_id:
        feedback_queryset = feedback_queryset.filter(category_id=category_id)
    if status:
        feedback_queryset = feedback_queryset.filter(status=status)
    
    # Order by most recent
    feedback_queryset = feedback_queryset.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(feedback_queryset, 10)  # 10 feedback items per page
    page_number = request.GET.get('page')
    feedback_list = paginator.get_page(page_number)
    
    # Get all categories for filter
    categories = Category.objects.all()
    
    context = {
        'feedback_list': feedback_list,
        'categories': categories,
    }
    
    return render(request, 'feedback/list.html', context)

@login_required
def feedback_detail(request, pk):
    """View to display feedback details"""
    feedback = get_object_or_404(Feedback, pk=pk)
    
    # Check if user has permission to view
    if not feedback.is_public and request.user != feedback.user and request.user.role != 'admin':
        return HttpResponseForbidden("You don't have permission to view this feedback.")
    
    context = {
        'feedback': feedback,
    }
    
    return render(request, 'feedback/detail.html', context)

@login_required
def feedback_create(request):
    """View to create new feedback"""
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            
            # Handle file uploads if any
            files = request.FILES.getlist('media')
            file_type = request.POST.get('file_type')
            
            for file in files:
                Media.objects.create(
                    feedback=feedback,
                    file_type=file_type,
                    file=file
                )
            
            messages.success(request, 'Your feedback has been submitted successfully!')
            return redirect('feedback_detail', pk=feedback.id)
    else:
        form = FeedbackForm()
    
    # Get all categories for dropdown
    categories = Category.objects.all()
    
    context = {
        'form': form,
        'categories': categories,
    }
    
    return render(request, 'feedback/create.html', context)

@login_required
def feedback_edit(request, pk):
    """View to edit existing feedback"""
    feedback = get_object_or_404(Feedback, pk=pk)
    
    # Check if user has permission to edit
    if request.user != feedback.user and request.user.role != 'admin':
        return HttpResponseForbidden("You don't have permission to edit this feedback.")
    
    if request.method == 'POST':
        form = FeedbackForm(request.POST, instance=feedback)
        if form.is_valid():
            form.save()
            
            messages.success(request, 'Your feedback has been updated successfully!')
            return redirect('feedback_detail', pk=feedback.id)
    else:
        form = FeedbackForm(instance=feedback)
    
    # Get all categories for dropdown
    categories = Category.objects.all()
    
    context = {
        'form': form,
        'feedback': feedback,
        'categories': categories,
    }
    
    return render(request, 'feedback/edit.html', context)

@login_required
def add_response(request, feedback_id):
    """View to add a response to feedback (admin only)"""
    feedback = get_object_or_404(Feedback, pk=feedback_id)
    
    # Check if user is admin
    if request.user.role != 'admin':
        return HttpResponseForbidden("Only administrators can add official responses.")
    
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.feedback = feedback
            response.responder = request.user
            response.save()
            
            messages.success(request, 'Your response has been added successfully!')
            return redirect('feedback_detail', pk=feedback_id)
    else:
        return HttpResponseForbidden("Method not allowed")
    
    return redirect('feedback_detail', pk=feedback_id)

@login_required
def update_feedback_status(request, feedback_id):
    """View to update feedback status (admin only)"""
    feedback = get_object_or_404(Feedback, pk=feedback_id)
    
    # Check if user is admin
    if request.user.role != 'admin':
        return HttpResponseForbidden("Only administrators can update feedback status.")
    
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in [s[0] for s in Feedback.STATUS_CHOICES]:
            feedback.status = status
            feedback.save()
            
            messages.success(request, f'Feedback status has been updated to {status}!')
        else:
            messages.error(request, 'Invalid status value')
    
    return redirect('feedback_detail', pk=feedback_id)

@login_required
def upload_media(request, feedback_id):
    """View to upload media for feedback"""
    feedback = get_object_or_404(Feedback, pk=feedback_id)
    
    # Check if user has permission to add media
    if request.user != feedback.user and request.user.role != 'admin':
        return HttpResponseForbidden("You don't have permission to add media to this feedback.")
    
    if request.method == 'POST':
        form = MediaForm(request.POST, request.FILES)
        if form.is_valid():
            media = form.save(commit=False)
            media.feedback = feedback
            media.save()
            
            messages.success(request, 'Media has been uploaded successfully!')
            return redirect('feedback_detail', pk=feedback_id)
    
    return redirect('feedback_detail', pk=feedback_id)