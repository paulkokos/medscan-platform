"""
Images models
"""
from django.db import models
from django.conf import settings


class MedicalImage(models.Model):
    """Model for medical images uploaded by users"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='medical_images/%Y/%m/%d/')
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    # Status
    analyzed = models.BooleanField(default=False)
    analysis_started_at = models.DateTimeField(null=True, blank=True)
    analysis_completed_at = models.DateTimeField(null=True, blank=True)

    # Metadata
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Image metadata
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    file_size = models.IntegerField(null=True, blank=True)  # in bytes

    class Meta:
        db_table = 'medical_images'
        ordering = ['-uploaded_at']
        verbose_name = 'Medical Image'
        verbose_name_plural = 'Medical Images'

    def __str__(self):
        return f"{self.title or 'Image'} - {self.user.email}"

    def save(self, *args, **kwargs):
        """Override save to extract image metadata"""
        if self.image:
            self.file_size = self.image.size
            # Extract dimensions if available
            try:
                from PIL import Image
                img = Image.open(self.image)
                self.width, self.height = img.size
            except Exception:
                pass

        super().save(*args, **kwargs)
