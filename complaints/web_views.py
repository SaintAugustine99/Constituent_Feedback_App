# complaints/web_views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.db.models import Q
from .models import Complaint
from .forms import ComplaintForm, StatusUpdateForm  # You'll need to create these forms

@login_required
def complaint_list(request):
    """View to display a list of complaints"""
    # Get filter parameters
    commission = request.GET.get('commission')
    status = request.GET.get('status')
    
    # Base queryset
    if request.user.role == 'admin':
        complaint_queryset = Complaint.objects.all()
    else:
        # For regular users, show only their own complaints
        complaint_queryset = Complaint.objects.filter(user=request.user)
    
    # Apply filters
    if commission:
        complaint_queryset = complaint_queryset.filter(commission_name__icontains=commission)
    if status:
        complaint_queryset = complaint_queryset.filter(status=status)
    
    # Order by most recent
    complaint_queryset = complaint_queryset.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(complaint_queryset, 10)  # 10 complaints per page
    page_number = request.GET.get('page')
    complaint_list = paginator.get_page(page_number)
    
    context = {
        'complaint_list': complaint_list,
    }
    
    return render(request, 'complaints/list.html', context)

@login_required
def complaint_detail(request, pk):
    """View to display complaint details"""
    complaint = get_object_or_404(Complaint, pk=pk)
    
    # Check if user has permission to view
    if request.user.role != 'admin' and complaint.user != request.user:
        return HttpResponseForbidden("You don't have permission to view this complaint.")
    
    context = {
        'complaint': complaint,
    }
    
    return render(request, 'complaints/detail.html', context)

@login_required
def complaint_create(request):
    """View to create new complaint"""
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user
            complaint.save()
            
            messages.success(request, 'Your complaint has been submitted successfully!')
            return redirect('complaint_detail', pk=complaint.id)
    else:
        form = ComplaintForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'complaints/create.html', context)

@login_required
def complaint_edit(request, pk):
    """View to edit existing complaint"""
    complaint = get_object_or_404(Complaint, pk=pk)
    
    # Check if user has permission to edit
    if request.user != complaint.user and request.user.role != 'admin':
        return HttpResponseForbidden("You don't have permission to edit this complaint.")
    
    if request.method == 'POST':
        form = ComplaintForm(request.POST, instance=complaint)
        if form.is_valid():
            form.save()
            
            messages.success(request, 'Your complaint has been updated successfully!')
            return redirect('complaint_detail', pk=complaint.id)
    else:
        form = ComplaintForm(instance=complaint)
    
    context = {
        'form': form,
        'complaint': complaint,
    }
    
    return render(request, 'complaints/edit.html', context)

@login_required
def update_complaint_status(request, pk):
    """View to update complaint status (admin only)"""
    complaint = get_object_or_404(Complaint, pk=pk)
    
    # Check if user is admin
    if request.user.role != 'admin':
        return HttpResponseForbidden("Only administrators can update complaint status.")
    
    if request.method == 'POST':
        form = StatusUpdateForm(request.POST, instance=complaint)
        if form.is_valid():
            form.save()
            
            messages.success(request, f"Complaint status has been updated to {complaint.get_status_display()}!")
            return redirect('complaint_detail', pk=pk)
    
    return redirect('complaint_detail', pk=pk)