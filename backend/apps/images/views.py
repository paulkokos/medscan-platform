"""
Images views
"""
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import MedicalImage
from .serializers import ImageSerializer, ImageUploadSerializer


class ImageViewSet(viewsets.ModelViewSet):
    """ViewSet for MedicalImage model"""

    permission_classes = (IsAuthenticated,)
    serializer_class = ImageSerializer

    def get_queryset(self):
        """Return images for current user only"""
        return MedicalImage.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        """Use different serializer for upload"""
        if self.action == "create":
            return ImageUploadSerializer
        return ImageSerializer

    def perform_create(self, serializer):
        """Save image with current user"""
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"])
    def start_analysis(self, request, pk=None):
        """Start analysis for an image"""
        image = self.get_object()

        if image.analyzed:
            return Response(
                {"error": "Image has already been analyzed"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # TODO: Trigger ML analysis task here
        # For now, just mark as started
        from django.utils import timezone

        image.analysis_started_at = timezone.now()
        image.save()

        return Response(
            {"message": "Analysis started", "image_id": image.id},
            status=status.HTTP_200_OK,
        )
