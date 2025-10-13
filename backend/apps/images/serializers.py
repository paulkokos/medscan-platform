"""
Images serializers
"""
from rest_framework import serializers
from .models import MedicalImage


class ImageSerializer(serializers.ModelSerializer):
    """Serializer for MedicalImage model"""

    user_email = serializers.EmailField(source="user.email", read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = MedicalImage
        fields = [
            "id",
            "user",
            "user_email",
            "image",
            "image_url",
            "title",
            "description",
            "analyzed",
            "analysis_started_at",
            "analysis_completed_at",
            "uploaded_at",
            "updated_at",
            "width",
            "height",
            "file_size",
        ]
        read_only_fields = [
            "id",
            "user",
            "analyzed",
            "analysis_started_at",
            "analysis_completed_at",
            "uploaded_at",
            "updated_at",
            "width",
            "height",
            "file_size",
        ]

    def get_image_url(self, obj):
        """Get full URL for image"""
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


class ImageUploadSerializer(serializers.ModelSerializer):
    """Serializer for uploading images"""

    class Meta:
        model = MedicalImage
        fields = ["image", "title", "description"]

    def validate_image(self, value):
        """Validate image file"""
        # Check file size (max 10MB)
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError("Image file size cannot exceed 10MB")

        # Check file extension
        allowed_extensions = ["jpg", "jpeg", "png", "dicom", "dcm"]
        extension = value.name.split(".")[-1].lower()
        if extension not in allowed_extensions:
            raise serializers.ValidationError(
                f'File extension "{extension}" is not allowed. '
                f'Allowed extensions are: {", ".join(allowed_extensions)}'
            )

        return value
