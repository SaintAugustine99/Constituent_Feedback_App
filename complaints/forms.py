# complaints/forms.py
from django import forms
from .models import Complaint

class ComplaintForm(forms.ModelForm):
    """Form for creating and editing complaints"""
    class Meta:
        model = Complaint
        fields = ['title', 'description', 'commission_name']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'commission_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class StatusUpdateForm(forms.ModelForm):
    """Form for updating complaint status (admin only)"""
    class Meta:
        model = Complaint
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
        }