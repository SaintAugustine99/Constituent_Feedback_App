from django.db import models
from django.conf import settings
from locations.models import Ward

class Project(models.Model):
    STATUS_CHOICES = [
        ('PLANNING', 'Planning'),
        ('ONGOING', 'Ongoing'),
        ('STALLED', 'Stalled'),
        ('COMPLETED', 'Completed'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, related_name='projects')
    budget_allocated = models.DecimalField(max_digits=12, decimal_places=2, help_text="Amount in KES")
    amount_spent = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    contractor_name = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PLANNING')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    completion_percentage = models.IntegerField(default=0)
    
    # Location (Optional Point)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.ward.name}"

class ProjectUpdate(models.Model):
    """Citizen Audit: Updates posted by users or officials"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='updates')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField()
    image = models.ImageField(upload_to='project_updates/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False, help_text="Verified by official/admin")

    def __str__(self):
        return f"Update on {self.project.name} by {self.user.username}"
