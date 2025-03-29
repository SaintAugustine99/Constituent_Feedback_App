from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from accounts.models import District
from django.utils import timezone

class Category(models.Model):
    """
    Model for organizing feedback by topic.
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    parent_category = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='subcategories')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"


class Feedback(models.Model):
    """
    Core entity for constituent submissions.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('under_review', 'Under Review'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='feedback')
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='feedback')
    sentiment_score = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    location_data = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title


class Response(models.Model):
    """
    Official responses to feedback.
    """
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE, related_name='responses')
    responder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='responses')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Response to {self.feedback.title}"
    
class Media(models.Model):
    """
    Attachments to feedback (photos, videos, audio).
    """
    MEDIA_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('document', 'Document'),
    ]

    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE, related_name='media')
    file_type = models.CharField(max_length=50, choices=MEDIA_TYPES)
    file = models.FileField(upload_to='feedback_media/')
    created_at = models.DateTimeField(auto_now_add=True, default=timezone.now)

    def __str__(self):
        return f"Media for {self.feedback.title}"

    class Meta:
        verbose_name_plural = "Media"