from django.db import models
from django.conf import settings
from django.utils import timezone
from locations.models import Constituency, Ward

class Docket(models.Model):
    """
    Represents the government entity responsible (e.g., Ministry of Health, Nairobi County Assembly).
    This answers 'WHO is asking for participation?'.
    """
    LEVEL_CHOICES = [
        ('NATIONAL_EXECUTIVE', 'National Executive (Ministries)'),
        ('NATIONAL_PARLIAMENT', 'Parliament (Senate/National Assembly)'),
        ('COUNTY_EXECUTIVE', 'County Executive'),
        ('COUNTY_ASSEMBLY', 'County Assembly'),
        ('JUDICIARY', 'Judiciary'),
        ('INDEPENDENT_COMMISSION', 'Independent Commission (IEBC, NEMA, etc.)'),
    ]

    name = models.CharField(max_length=255, help_text="e.g. Ministry of ICT or Nairobi City County")
    level = models.CharField(max_length=50, choices=LEVEL_CHOICES)
    website_url = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_level_display()})"

class InstrumentCategory(models.Model):
    """
    Classifies the type of law/policy.
    e.g., 'Proposed Bill', 'Finance Bill', 'Regulation', 'CIDP'.
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, help_text="Legal definition/context for this category")

    def __str__(self):
        return self.name

class LegalInstrument(models.Model):
    """
    The core item requiring participation.
    """
    STATUS_CHOICES = [
        ('DRAFT', 'Draft / Internal Review'),
        ('GAZETTED', 'Gazetted / Published'),
        ('PUBLIC_PARTICIPATION', 'Open for Public Views'),
        ('COMMITTEE_STAGE', 'Committee Review'),
        ('PASSED', 'Passed / Enacted'),
        ('REJECTED', 'Rejected / Withdrawn'),
    ]

    title = models.CharField(max_length=300, help_text="e.g. The Finance Bill 2026")
    docket = models.ForeignKey(Docket, on_delete=models.CASCADE, related_name='instruments')
    category = models.ForeignKey(InstrumentCategory, on_delete=models.PROTECT)
    
    # The 'Reasonable Time' tracking
    published_date = models.DateField(default=timezone.now)
    participation_deadline = models.DateField(help_text="The cutoff date for public submissions")
    
    # Documents
    legal_text_url = models.URLField(help_text="Link to the PDF of the Bill/Policy")
    summary_text = models.TextField(help_text="A simplified summary for the public")
    
    current_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='DRAFT')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_open(self):
        """Check if we are still within the participation window"""
        return self.current_status == 'PUBLIC_PARTICIPATION' and self.participation_deadline >= timezone.now().date()

    def __str__(self):
        return self.title

class StatusReport(models.Model):
    """
    Updates from the dockets.
    e.g. 'First Reading done', 'Stakeholder forum scheduled for Tuesday'.
    """
    instrument = models.ForeignKey(LegalInstrument, on_delete=models.CASCADE, related_name='status_reports')
    title = models.CharField(max_length=200)
    content = models.TextField()
    report_date = models.DateTimeField(auto_now_add=True)
    attachment = models.FileField(upload_to='status_reports/', blank=True, null=True)

    class Meta:
        ordering = ['-report_date']

class PublicFeedback(models.Model):
    """
    The Constituent's input.
    Includes text, sentiment (for analysis), and image evidence.
    """
    instrument = models.ForeignKey(LegalInstrument, on_delete=models.CASCADE, related_name='feedback')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True) # Optional: Allow anonymous?
    
    # The actual feedback
    full_name = models.CharField(max_length=150)
    constituency = models.CharField(max_length=150, blank=True)
    ward = models.CharField(max_length=150, blank=True)

    # Structured location references
    constituency_ref = models.ForeignKey(Constituency, on_delete=models.SET_NULL, null=True, blank=True, related_name='feedback')
    ward_ref = models.ForeignKey(Ward, on_delete=models.SET_NULL, null=True, blank=True, related_name='feedback')

    position = models.CharField(max_length=20, choices=[('SUPPORT', 'Support'), ('OPPOSE', 'Oppose'), ('AMEND', 'Propose Amendments')])
    comments = models.TextField()

    # Amendment-specific fields
    target_clause = models.CharField(max_length=200, blank=True, help_text="Which clause/section to amend")
    proposed_alternative = models.TextField(blank=True, help_text="Proposed alternative text")

    # Evidence / Multimedia
    image_evidence = models.ImageField(upload_to='feedback_evidence/', blank=True, null=True, help_text="Upload photos (e.g. current state of road for CIDP)")

    # Meta
    submitted_at = models.DateTimeField(auto_now_add=True)

    # For automated analysis later
    is_verified = models.BooleanField(default=False) 

    def __str__(self):
        return f"Feedback on {self.instrument.title} by {self.full_name}"
