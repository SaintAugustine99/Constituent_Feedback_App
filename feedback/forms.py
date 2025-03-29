# feedback/forms.py
from django import forms
from .models import Feedback, Response, Media, Category

class FeedbackForm(forms.ModelForm):
    """Form for creating and editing feedback"""
    # Extra fields that aren't directly in the model
    location_address = forms.CharField(max_length=255, required=False, 
                                      widget=forms.TextInput(attrs={'class': 'form-control'}))
    location_lat = forms.FloatField(required=False, widget=forms.HiddenInput())
    location_lng = forms.FloatField(required=False, widget=forms.HiddenInput())
    
    class Meta:
        model = Feedback
        fields = ['title', 'description', 'category', 'is_public']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make category optional
        self.fields['category'].required = False
        
        # If we're editing an existing feedback with location_data
        if self.instance.pk and self.instance.location_data:
            if 'address' in self.instance.location_data:
                self.fields['location_address'].initial = self.instance.location_data['address']
            if 'lat' in self.instance.location_data and 'lng' in self.instance.location_data:
                self.fields['location_lat'].initial = self.instance.location_data['lat']
                self.fields['location_lng'].initial = self.instance.location_data['lng']
    
    def save(self, commit=True):
        feedback = super().save(commit=False)
        
        # Process location data
        location_data = {}
        if self.cleaned_data.get('location_address'):
            location_data['address'] = self.cleaned_data['location_address']
        if self.cleaned_data.get('location_lat') and self.cleaned_data.get('location_lng'):
            location_data['lat'] = self.cleaned_data['location_lat']
            location_data['lng'] = self.cleaned_data['location_lng']
        
        if location_data:
            feedback.location_data = location_data
        
        if commit:
            feedback.save()
        
        return feedback

class ResponseForm(forms.ModelForm):
    """Form for adding responses to feedback"""
    class Meta:
        model = Response
        fields = ['content', 'is_public']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class MediaForm(forms.ModelForm):
    """Form for uploading media attachments"""
    class Meta:
        model = Media
        fields = ['file', 'file_type']
        widgets = {
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'file_type': forms.Select(attrs={'class': 'form-select'}),
        }