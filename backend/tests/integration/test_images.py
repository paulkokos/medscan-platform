"""
Integration tests for images API endpoints
"""
import pytest
from django.urls import reverse
from rest_framework import status
from apps.images.models import MedicalImage


@pytest.mark.images
@pytest.mark.integration
class TestImageList:
    """Test image listing endpoint"""

    def test_list_images_authenticated(self, authenticated_client, user, create_medical_image, sample_image):
        """Test listing images when authenticated"""
        # Create some images for the user
        create_medical_image(user=user, title='Image 1', image=sample_image)
        create_medical_image(user=user, title='Image 2', image=sample_image)

        url = reverse('images-list')
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 2

    def test_list_images_unauthenticated(self, api_client):
        """Test listing images without authentication"""
        url = reverse('images-list')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_images_only_user_images(self, authenticated_client, user, create_user, create_medical_image, sample_image):
        """Test that users only see their own images"""
        # Create images for current user
        create_medical_image(user=user, title='My Image', image=sample_image)

        # Create images for another user
        other_user = create_user(email='other@example.com')
        create_medical_image(user=other_user, title='Other Image', image=sample_image)

        url = reverse('images-list')
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['title'] == 'My Image'


@pytest.mark.images
@pytest.mark.integration
class TestImageUpload:
    """Test image upload endpoint"""

    def test_upload_image_success(self, authenticated_client, sample_image):
        """Test successful image upload"""
        url = reverse('images-list')
        data = {
            'title': 'Test Brain Scan',
            'description': 'MRI scan of the brain',
            'image': sample_image
        }

        response = authenticated_client.post(url, data, format='multipart')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == 'Test Brain Scan'
        assert response.data['description'] == 'MRI scan of the brain'
        assert MedicalImage.objects.filter(title='Test Brain Scan').exists()

    def test_upload_image_without_file(self, authenticated_client):
        """Test upload without image file"""
        url = reverse('images-list')
        data = {
            'title': 'Test Scan'
        }

        response = authenticated_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_upload_image_unauthenticated(self, api_client, sample_image):
        """Test upload without authentication"""
        url = reverse('images-list')
        data = {
            'title': 'Test Scan',
            'image': sample_image
        }

        response = api_client.post(url, data, format='multipart')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.images
@pytest.mark.integration
class TestImageDetail:
    """Test image detail endpoint"""

    def test_get_image_detail(self, authenticated_client, create_medical_image, user, sample_image):
        """Test getting image details"""
        image = create_medical_image(user=user, title='Detail Test', image=sample_image)
        url = reverse('images-detail', kwargs={'pk': image.id})

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == image.id
        assert response.data['title'] == 'Detail Test'

    def test_get_other_user_image(self, authenticated_client, create_user, create_medical_image, sample_image):
        """Test accessing another user's image"""
        other_user = create_user(email='other@example.com')
        image = create_medical_image(user=other_user, title='Other Image', image=sample_image)
        url = reverse('images-detail', kwargs={'pk': image.id})

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_nonexistent_image(self, authenticated_client):
        """Test getting non-existent image"""
        url = reverse('images-detail', kwargs={'pk': 99999})

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.images
@pytest.mark.integration
class TestImageUpdate:
    """Test image update endpoint"""

    def test_update_image(self, authenticated_client, create_medical_image, user, sample_image):
        """Test updating image metadata"""
        image = create_medical_image(user=user, title='Original Title', image=sample_image)
        url = reverse('images-detail', kwargs={'pk': image.id})
        data = {
            'title': 'Updated Title',
            'description': 'Updated description'
        }

        response = authenticated_client.patch(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Updated Title'
        assert response.data['description'] == 'Updated description'

        image.refresh_from_db()
        assert image.title == 'Updated Title'

    def test_update_other_user_image(self, authenticated_client, create_user, create_medical_image, sample_image):
        """Test updating another user's image"""
        other_user = create_user(email='other@example.com')
        image = create_medical_image(user=other_user, title='Other Image', image=sample_image)
        url = reverse('images-detail', kwargs={'pk': image.id})
        data = {'title': 'Hacked Title'}

        response = authenticated_client.patch(url, data, format='json')

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.images
@pytest.mark.integration
class TestImageDelete:
    """Test image deletion endpoint"""

    def test_delete_image(self, authenticated_client, create_medical_image, user, sample_image):
        """Test deleting own image"""
        image = create_medical_image(user=user, title='To Delete', image=sample_image)
        image_id = image.id
        url = reverse('images-detail', kwargs={'pk': image_id})

        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not MedicalImage.objects.filter(id=image_id).exists()

    def test_delete_other_user_image(self, authenticated_client, create_user, create_medical_image, sample_image):
        """Test deleting another user's image"""
        other_user = create_user(email='other@example.com')
        image = create_medical_image(user=other_user, title='Other Image', image=sample_image)
        url = reverse('images-detail', kwargs={'pk': image.id})

        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert MedicalImage.objects.filter(id=image.id).exists()


@pytest.mark.images
@pytest.mark.integration
class TestImageAnalysis:
    """Test image analysis endpoint"""

    def test_start_analysis(self, authenticated_client, create_medical_image, user, sample_image):
        """Test starting image analysis"""
        image = create_medical_image(user=user, title='To Analyze', image=sample_image)
        url = reverse('images-start-analysis', kwargs={'pk': image.id})

        response = authenticated_client.post(url)

        assert response.status_code == status.HTTP_200_OK
        assert 'message' in response.data
        assert response.data['image_id'] == image.id

        image.refresh_from_db()
        assert image.analysis_started_at is not None

    def test_start_analysis_already_analyzed(self, authenticated_client, create_medical_image, user, sample_image):
        """Test starting analysis on already analyzed image"""
        from django.utils import timezone

        image = create_medical_image(
            user=user,
            title='Already Analyzed',
            image=sample_image,
            analyzed=True,
            analysis_started_at=timezone.now()
        )
        url = reverse('images-start-analysis', kwargs={'pk': image.id})

        response = authenticated_client.post(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data

    def test_start_analysis_other_user_image(self, authenticated_client, create_user, create_medical_image, sample_image):
        """Test starting analysis on another user's image"""
        other_user = create_user(email='other@example.com')
        image = create_medical_image(user=other_user, title='Other Image', image=sample_image)
        url = reverse('images-start-analysis', kwargs={'pk': image.id})

        response = authenticated_client.post(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
