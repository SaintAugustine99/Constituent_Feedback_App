from django.db import models

class County(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=3, unique=True, help_text="e.g., 047 for Nairobi")

    class Meta:
        verbose_name_plural = " Counties" # Space hack to force top ordering
        ordering = ['name']

    def __str__(self):
        return f"{self.code} - {self.name}"

class Constituency(models.Model):
    county = models.ForeignKey(County, on_delete=models.CASCADE, related_name='constituencies')
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Constituencies"
        ordering = ['name']
        unique_together = ['county', 'name'] # Prevents duplicates within a county

    def __str__(self):
        return f"{self.name} ({self.county.name})"

class Ward(models.Model):
    constituency = models.ForeignKey(Constituency, on_delete=models.CASCADE, related_name='wards')
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']
        unique_together = ['constituency', 'name']

    def __str__(self):
        return f"{self.name} - {self.constituency.name}"

class Official(models.Model):
    TITLE_CHOICES = [
        ('MCA', 'Member of County Assembly'),
        ('MP', 'Member of Parliament'),
        ('GOV', 'Governor'),
        ('SEN', 'Senator'),
        ('WOMAN_REP', 'Woman Representative'),
    ]

    name = models.CharField(max_length=255)
    title = models.CharField(max_length=20, choices=TITLE_CHOICES)
    photo = models.ImageField(upload_to='officials/', blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, help_text="Public contact number")
    email = models.EmailField(blank=True, help_text="Public email address")
    whatsapp_link = models.URLField(blank=True, help_text="Direct WhatsApp API link")
    
    # Jurisdiction
    ward = models.ForeignKey(Ward, on_delete=models.SET_NULL, null=True, blank=True, related_name='officials')
    constituency = models.ForeignKey(Constituency, on_delete=models.SET_NULL, null=True, blank=True, related_name='officials')
    county = models.ForeignKey(County, on_delete=models.SET_NULL, null=True, blank=True, related_name='officials')

    def __str__(self):
        return f"{self.name} ({self.get_title_display()})"
