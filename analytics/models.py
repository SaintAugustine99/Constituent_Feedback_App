from django.db import models

# Create your models here.
from django.db import models

# Models for storing analytics results if needed
class SentimentAnalysisResult(models.Model):
    """
    Stores pre-computed sentiment analysis results
    """
    feedback = models.OneToOneField('feedback.Feedback', on_delete=models.CASCADE, related_name='sentiment_results')
    sentiment_score = models.FloatField()
    processed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Sentiment for {self.feedback.title}"