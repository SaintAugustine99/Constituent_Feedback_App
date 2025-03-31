# accounts/web_views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from .models import User, District
from .forms import LoginForm, RegistrationForm, ProfileForm  # You'll need to create these forms
from feedback.models import Feedback
from complaints.models import Complaint

def login_view(request):
    """View for user login"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                login(request, user)
                # Redirect to the next page if specified, otherwise go to home
                next_page = request.GET.get('next', 'home')
                return redirect(next_page)
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})

def register_view(request):
    """View for user registration"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Log the user in
            login(request, user)
            
            messages.success(request, 'Registration successful! Welcome to the platform.')
            return redirect('home')
    else:
        form = RegistrationForm()
    
    # Get all districts for dropdown
    districts = District.objects.all()
    
    context = {
        'form': form,
        'districts': districts,
    }
    
    return render(request, 'accounts/register.html', context)

@login_required
def profile_view(request):
    """View to display the user's profile"""
    # Get user's feedback and complaints
    user_feedback = Feedback.objects.filter(user=request.user).order_by('-created_at')
    user_complaints = Complaint.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'user_feedback': user_feedback,
        'user_complaints': user_complaints,
    }
    
    return render(request, 'accounts/profile.html', context)

@login_required
def edit_profile_view(request):
    """View to edit user profile"""
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    
    # Get all districts for dropdown
    districts = District.objects.all()
    
    context = {
        'form': form,
        'districts': districts,
    }
    
    return render(request, 'accounts/edit_profile.html', context)
def logout_view(request):
    """View for user logout"""
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')