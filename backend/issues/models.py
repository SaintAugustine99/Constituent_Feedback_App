from django.db import models
from django.conf import settings

class ServiceRequest(models.Model):
    CATEGORY_CHOICES = [
        ('ROAD', 'Roads & Transport'),
        ('WATER', 'Water & Sanitation'),
        ('POWER', 'Power & Lighting'),
        ('SECURITY', 'Security & Safety'),
        ('ENV', 'Environment & Garbage'),
        ('OTHER', 'Other'),
    ]

    STATUS_CHOICES = [
        ('REPORTED', 'Reported'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='service_requests')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    image_evidence = models.ImageField(upload_to='issues/', blank=True, null=True)
    
    # Location (Optional GPS, defaults to User's Ward in logic)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    location_description = models.CharField(max_length=255, blank=True, help_text="e.g. Near Main Market")

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='REPORTED')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_category_display()} - {self.created_at.strftime('%Y-%m-%d')}"
