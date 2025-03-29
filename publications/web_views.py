# publications/web_views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Gazette, Report
from feedback.models import Category
from .forms import GazetteForm, ReportForm  # You'll need to create these forms

@login_required
def gazette_list(request):
    """View to display a list of gazettes"""
    # Get filter parameters
    title = request.GET.get('title')
    category_id = request.GET.get('category')
    date = request.GET.get('date')
    
    # Base queryset
    gazette_queryset = Gazette.objects.all()
    
    # Apply filters
    if title:
        gazette_queryset = gazette_queryset.filter(title__icontains=title)
    if category_id:
        gazette_queryset = gazette_queryset.filter(category_id=category_id)
    if date:
        gazette_queryset = gazette_queryset.filter(publish_date=date)
    
    # Order by most recent
    gazette_queryset = gazette_queryset.order_by('-publish_date')
    
    # Pagination
    paginator = Paginator(gazette_queryset, 10)  # 10 gazettes per page
    page_number = request.GET.get('page')
    gazette_list = paginator.get_page(page_number)
    
    # Get all categories for filter
    categories = Category.objects.all()
    
    context = {
        'gazette_list': gazette_list,
        'categories': categories,
    }
    
    return render(request, 'publications/gazette_list.html', context)

@login_required
def gazette_detail(request, pk):
    """View to display gazette details"""
    gazette = get_object_or_404(Gazette, pk=pk)
    
    context = {
        'gazette': gazette,
    }
    
    return render(request, 'publications/gazette_detail.html', context)

@login_required
def gazette_create(request):
    """View to create new gazette (admin only)"""
    # Check if user is admin
    if request.user.role != 'admin':
        return HttpResponseForbidden("Only administrators can create gazettes.")
    
    if request.method == 'POST':
        form = GazetteForm(request.POST)
        if form.is_valid():
            form.save()
            
            messages.success(request, 'Gazette has been created successfully!')
            return redirect('gazette_list')
    else:
        form = GazetteForm()
    
    # Get all categories for dropdown
    categories = Category.objects.all()
    
    context = {
        'form': form,
        'categories': categories,
    }
    
    return render(request, 'publications/gazette_create.html', context)

@login_required
def gazette_edit(request, pk):
    """View to edit existing gazette (admin only)"""
    # Check if user is admin
    if request.user.role != 'admin':
        return HttpResponseForbidden("Only administrators can edit gazettes.")
    
    gazette = get_object_or_404(Gazette, pk=pk)
    
    if request.method == 'POST':
        form = GazetteForm(request.POST, instance=gazette)
        if form.is_valid():
            form.save()
            
            messages.success(request, 'Gazette has been updated successfully!')
            return redirect('gazette_detail', pk=gazette.id)
    else:
        form = GazetteForm(instance=gazette)
    
    # Get all categories for dropdown
    categories = Category.objects.all()
    
    context = {
        'form': form,
        'gazette': gazette,
        'categories': categories,
    }
    
    return render(request, 'publications/gazette_edit.html', context)

@login_required
def report_list(request):
    """View to display a list of reports"""
    # Get filter parameters
    title = request.GET.get('title')
    institution = request.GET.get('institution')
    year = request.GET.get('year')
    category_id = request.GET.get('category')
    
    # Base queryset
    report_queryset = Report.objects.all()
    
    # Apply filters
    if title:
        report_queryset = report_queryset.filter(title__icontains=title)
    if institution:
        report_queryset = report_queryset.filter(institution_name__icontains=institution)
    if year:
        report_queryset = report_queryset.filter(report_year=year)
    if category_id:
        report_queryset = report_queryset.filter(category_id=category_id)
    
    # Order by most recent
    report_queryset = report_queryset.order_by('-report_year')
    
    # Pagination
    paginator = Paginator(report_queryset, 10)  # 10 reports per page
    page_number = request.GET.get('page')
    report_list = paginator.get_page(page_number)
    
    # Get all categories for filter
    categories = Category.objects.all()
    
    # Get unique years for filter
    years = Report.objects.values_list('report_year', flat=True).distinct().order_by('-report_year')
    
    context = {
        'report_list': report_list,
        'categories': categories,
        'years': years,
    }
    
    return render(request, 'publications/report_list.html', context)

@login_required
def report_detail(request, pk):
    """View to display report details"""
    report = get_object_or_404(Report, pk=pk)
    
    context = {
        'report': report,
    }
    
    return render(request, 'publications/report_detail.html', context)

@login_required
def report_create(request):
    """View to create new report (admin only)"""
    # Check if user is admin
    if request.user.role != 'admin':
        return HttpResponseForbidden("Only administrators can create reports.")
    
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            form.save()
            
            messages.success(request, 'Report has been created successfully!')
            return redirect('report_list')
    else:
        form = ReportForm()
    
    # Get all categories for dropdown
    categories = Category.objects.all()
    
    context = {
        'form': form,
        'categories': categories,
    }
    
    return render(request, 'publications/report_create.html', context)

@login_required
def report_edit(request, pk):
    """View to edit existing report (admin only)"""
    # Check if user is admin
    if request.user.role != 'admin':
        return HttpResponseForbidden("Only administrators can edit reports.")
    
    report = get_object_or_404(Report, pk=pk)
    
    if request.method == 'POST':
        form = ReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            
            messages.success(request, 'Report has been updated successfully!')
            return redirect('report_detail', pk=report.id)
    else:
        form = ReportForm(instance=report)
    
    # Get all categories for dropdown
    categories = Category.objects.all()
    
    context = {
        'form': form,
        'report': report,
        'categories': categories,
    }
    
    return render(request, 'publications/report_edit.html', context)