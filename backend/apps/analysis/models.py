"""
Analysis models
"""
from django.db import models
from apps.images.models import MedicalImage


class Analysis(models.Model):
    """Model for image analysis results"""

    image = models.OneToOneField(
        MedicalImage,
        on_delete=models.CASCADE,
        related_name='analysis'
    )

    # Analysis results
    results = models.JSONField(default=dict, blank=True)

    # Metrics
    dice_score = models.FloatField(null=True, blank=True)
    iou_score = models.FloatField(null=True, blank=True)
    precision = models.FloatField(null=True, blank=True)
    recall = models.FloatField(null=True, blank=True)

    # Processing info
    processing_time = models.FloatField(null=True, blank=True)  # in seconds
    model_version = models.CharField(max_length=50, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'analysis_results'
        ordering = ['-created_at']
        verbose_name = 'Analysis'
        verbose_name_plural = 'Analyses'

    def __str__(self):
        return f"Analysis for {self.image.title or 'Image'} (ID: {self.image.id})"
