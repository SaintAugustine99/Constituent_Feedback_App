# publications/forms.py
from django import forms
from .models import Gazette, Report

class GazetteForm(forms.ModelForm):
    """Form for creating and editing gazettes"""
    class Meta:
        model = Gazette
        fields = ['title', 'description', 'document_url', 'publish_date', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'document_url': forms.URLInput(attrs={'class': 'form-control'}),
            'publish_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }

class ReportForm(forms.ModelForm):
    """Form for creating and editing reports"""
    class Meta:
        model = Report
        fields = ['title', 'institution_name', 'report_year', 'document_url', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'institution_name': forms.TextInput(attrs={'class': 'form-control'}),
            'report_year': forms.NumberInput(attrs={'class': 'form-control', 'min': '1900', 'max': '2099'}),
            'document_url': forms.URLInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }