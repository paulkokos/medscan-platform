"""
Unit tests for database models
"""
import pytest
from apps.analysis.models import Analysis
from apps.images.models import MedicalImage
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


@pytest.mark.unit
class TestUserModel:
    """Test User model"""

    def test_create_user(self, db):
        """Test creating a user"""
        user = User.objects.create_user(
            email="test@example.com",
            password="TestPass123!",
            first_name="Test",
            last_name="User",
        )

        assert user.email == "test@example.com"
        assert user.first_name == "Test"
        assert user.last_name == "User"
        assert user.is_active is True
        assert user.is_staff is False
        assert user.is_superuser is False
        assert user.check_password("TestPass123!")

    def test_create_superuser(self, db):
        """Test creating a superuser"""
        admin = User.objects.create_superuser(
            email="admin@example.com", password="AdminPass123!"
        )

        assert admin.is_staff is True
        assert admin.is_superuser is True
        assert admin.is_active is True

    def test_user_str_representation(self, user):
        """Test user string representation"""
        assert str(user) == "john@example.com"

    def test_user_get_full_name(self, user):
        """Test get_full_name method"""
        assert user.get_full_name() == "John Doe"

    def test_user_get_short_name(self, user):
        """Test get_short_name method"""
        assert user.get_short_name() == "John"

    def test_user_email_normalization(self, db):
        """Test that email domain is normalized"""
        email = "Test@EXAMPLE.COM"
        user = User.objects.create_user(email=email, password="TestPass123!")

        # Django normalizes the domain but not the local part
        assert user.email == "Test@example.com"

    def test_user_without_email_fails(self, db):
        """Test that creating user without email raises error"""
        with pytest.raises(ValueError):
            User.objects.create_user(email="", password="TestPass123!")


@pytest.mark.unit
class TestMedicalImageModel:
    """Test MedicalImage model"""

    def test_create_medical_image(self, user, sample_image):
        """Test creating a medical image"""
        image = MedicalImage.objects.create(
            user=user,
            title="Test MRI Scan",
            description="Brain MRI scan",
            image=sample_image,
        )

        assert image.user == user
        assert image.title == "Test MRI Scan"
        assert image.description == "Brain MRI scan"
        assert image.analyzed is False
        assert image.analysis_started_at is None
        assert image.uploaded_at is not None
        assert image.updated_at is not None

    def test_medical_image_str_representation(
        self, create_medical_image, user, sample_image
    ):
        """Test medical image string representation"""
        image = create_medical_image(user=user, title="Brain Scan", image=sample_image)

        assert "Brain Scan" in str(image)

    def test_medical_image_ordering(self, user, sample_image):
        """Test that images are ordered by upload date (newest first)"""
        import time

        image1 = MedicalImage.objects.create(
            user=user, title="First Image", image=sample_image
        )

        time.sleep(0.1)

        image2 = MedicalImage.objects.create(
            user=user, title="Second Image", image=sample_image
        )

        images = list(MedicalImage.objects.all())
        assert images[0].id == image2.id
        assert images[1].id == image1.id

    def test_medical_image_file_metadata(self, user, sample_image):
        """Test that file metadata is extracted"""
        image = MedicalImage.objects.create(
            user=user, title="Test scan", image=sample_image
        )

        # Check that metadata was extracted
        assert image.file_size is not None
        assert image.width is not None
        assert image.height is not None

    def test_medical_image_analysis_started(
        self, create_medical_image, user, sample_image
    ):
        """Test marking image analysis as started"""
        image = create_medical_image(user=user, title="Test", image=sample_image)

        now = timezone.now()
        image.analysis_started_at = now
        image.save()

        image.refresh_from_db()
        assert image.analysis_started_at is not None

    def test_medical_image_analyzed_flag(
        self, create_medical_image, user, sample_image
    ):
        """Test analyzed flag"""
        image = create_medical_image(user=user, title="Test", image=sample_image)

        assert image.analyzed is False

        image.analyzed = True
        image.save()

        image.refresh_from_db()
        assert image.analyzed is True


@pytest.mark.unit
class TestAnalysisModel:
    """Test Analysis model"""

    def test_create_analysis(self, create_medical_image, user, sample_image):
        """Test creating an analysis"""
        image = create_medical_image(user=user, title="Test", image=sample_image)

        analysis = Analysis.objects.create(
            image=image,
            results={"segmentation": "data"},
            dice_score=0.85,
            iou_score=0.78,
            precision=0.90,
            recall=0.82,
            processing_time=5.2,
            model_version="v1.0",
        )

        assert analysis.image == image
        assert analysis.results == {"segmentation": "data"}
        assert analysis.dice_score == 0.85
        assert analysis.iou_score == 0.78
        assert analysis.precision == 0.90
        assert analysis.recall == 0.82
        assert analysis.processing_time == 5.2
        assert analysis.model_version == "v1.0"

    def test_analysis_str_representation(
        self, create_medical_image, user, sample_image
    ):
        """Test analysis string representation"""
        image = create_medical_image(user=user, title="Brain MRI", image=sample_image)
        analysis = Analysis.objects.create(image=image)

        assert "Brain MRI" in str(analysis)
        assert str(image.id) in str(analysis)

    def test_analysis_one_to_one_relationship(
        self, create_medical_image, user, sample_image
    ):
        """Test that image can only have one analysis"""
        image = create_medical_image(user=user, title="Test", image=sample_image)

        # Create first analysis
        analysis1 = Analysis.objects.create(image=image)

        # Try to create second analysis for same image
        with pytest.raises(Exception):  # Should raise IntegrityError
            Analysis.objects.create(image=image)

    def test_analysis_cascade_delete(self, create_medical_image, user, sample_image):
        """Test that analysis is deleted when image is deleted"""
        image = create_medical_image(user=user, title="Test", image=sample_image)
        analysis = Analysis.objects.create(image=image)
        analysis_id = analysis.id

        # Delete the image
        image.delete()

        # Analysis should also be deleted
        assert not Analysis.objects.filter(id=analysis_id).exists()

    def test_analysis_default_results(self, create_medical_image, user, sample_image):
        """Test that results defaults to empty dict"""
        image = create_medical_image(user=user, title="Test", image=sample_image)
        analysis = Analysis.objects.create(image=image)

        assert analysis.results == {}

    def test_analysis_ordering(self, user, sample_image):
        """Test that analyses are ordered by creation date (newest first)"""
        import time

        from apps.images.models import MedicalImage

        image1 = MedicalImage.objects.create(
            user=user, title="Image 1", image=sample_image
        )
        analysis1 = Analysis.objects.create(image=image1)

        time.sleep(0.1)

        image2 = MedicalImage.objects.create(
            user=user, title="Image 2", image=sample_image
        )
        analysis2 = Analysis.objects.create(image=image2)

        analyses = list(Analysis.objects.all())
        assert analyses[0].id == analysis2.id
        assert analyses[1].id == analysis1.id

    def test_analysis_metrics_nullable(self, create_medical_image, user, sample_image):
        """Test that metric fields can be null"""
        image = create_medical_image(user=user, title="Test", image=sample_image)
        analysis = Analysis.objects.create(image=image)

        assert analysis.dice_score is None
        assert analysis.iou_score is None
        assert analysis.precision is None
        assert analysis.recall is None
        assert analysis.processing_time is None
