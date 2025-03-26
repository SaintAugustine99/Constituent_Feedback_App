from django.db import models

# Create your models here.

from django.db import models
from django.conf import settings

class Complaint(models.Model):
    """
    Formal complaints to ombudsman or commissions.
    """
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('resolved', 'Resolved'),
        ('dismissed', 'Dismissed'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='complaints')
    title = models.CharField(max_length=200)
    description = models.TextField()
    commission_name = models.CharField(max_length=200, help_text="Name of the ombudsman or commission")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title