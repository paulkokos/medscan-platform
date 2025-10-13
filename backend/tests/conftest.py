"""
Pytest configuration and fixtures
"""
import io

import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


@pytest.fixture
def api_client():
    """Return API client"""
    return APIClient()


@pytest.fixture
def create_user(db):
    """Factory fixture to create users"""

    def make_user(**kwargs):
        if "email" not in kwargs:
            kwargs["email"] = "testuser@example.com"
        if "password" not in kwargs:
            kwargs["password"] = "TestPass123!"

        password = kwargs.pop("password")
        user = User.objects.create_user(**kwargs)
        user.set_password(password)
        user.save()
        return user

    return make_user


@pytest.fixture
def user(create_user):
    """Create a standard test user"""
    return create_user(
        email="john@example.com",
        first_name="John",
        last_name="Doe",
        password="TestPass123!",
    )


@pytest.fixture
def admin_user(create_user):
    """Create an admin user"""
    return create_user(
        email="admin@example.com",
        first_name="Admin",
        last_name="User",
        password="AdminPass123!",
        is_staff=True,
        is_superuser=True,
    )


@pytest.fixture
def authenticated_client(api_client, user):
    """Return an authenticated API client"""
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return api_client


@pytest.fixture
def admin_client(api_client, admin_user):
    """Return an authenticated admin API client"""
    refresh = RefreshToken.for_user(admin_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return api_client


@pytest.fixture
def sample_image():
    """Create a sample image file for testing"""
    # Create a simple test image
    image = Image.new("RGB", (100, 100), color="red")
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)

    return SimpleUploadedFile(
        name="test_image.png", content=buffer.read(), content_type="image/png"
    )


@pytest.fixture
def sample_dicom_file():
    """Create a mock DICOM file for testing"""
    # Simple binary content to simulate DICOM
    content = b"DICM" + b"\x00" * 100
    return SimpleUploadedFile(
        name="test_scan.dcm", content=content, content_type="application/dicom"
    )


@pytest.fixture
def create_medical_image(db, user):
    """Factory fixture to create medical images"""
    from apps.images.models import MedicalImage

    def make_image(**kwargs):
        if "user" not in kwargs:
            kwargs["user"] = user
        if "title" not in kwargs:
            kwargs["title"] = "Test Medical Image"

        return MedicalImage.objects.create(**kwargs)

    return make_image


@pytest.fixture
def medical_image(create_medical_image, sample_image):
    """Create a test medical image"""
    return create_medical_image(
        title="Brain MRI Scan", description="Test MRI scan of brain", image=sample_image
    )


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """Enable database access for all tests"""
    pass
