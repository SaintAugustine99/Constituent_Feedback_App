from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from feedback.models import Category

class Gazette(models.Model):
    """
    Government publications for public review.
    """
    title = models.CharField(max_length=200)
    description = models.TextField()
    document_url = models.URLField()
    publish_date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='gazettes')
    
    def __str__(self):
        return self.title

class Report(models.Model):
    """
    Annual institutional reports.
    """
    title = models.CharField(max_length=200)
    institution_name = models.CharField(max_length=200)
    report_year = models.IntegerField()
    document_url = models.URLField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='reports')
    
    def __str__(self):
        return f"{self.institution_name} - {self.title} ({self.report_year})"