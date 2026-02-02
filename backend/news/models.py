from django.db import models


class GovernmentResource(models.Model):
    CATEGORY_CHOICES = [
        ('LEGAL', 'Legal & Regulatory'),
        ('LEGISLATIVE', 'Legislative'),
        ('ELECTORAL', 'Electoral'),
        ('DATA', 'Data & Statistics'),
        ('SERVICES', 'Government Services'),
    ]

    name = models.CharField(max_length=200)
    url = models.URLField()
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='SERVICES')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class NewsArticle(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    source_name = models.CharField(max_length=500)
    url = models.URLField(unique=True)
    image_url = models.URLField(blank=True)
    published_at = models.DateTimeField()

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return self.title
