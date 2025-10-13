"""
Integration tests for authentication endpoints
"""
import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.auth
@pytest.mark.integration
class TestUserRegistration:
    """Test user registration"""

    def test_register_user_success(self, api_client):
        """Test successful user registration"""
        url = reverse("register")
        data = {
            "email": "newuser@example.com",
            "password": "SecurePass123!",
            "password2": "SecurePass123!",
            "first_name": "Jane",
            "last_name": "Smith",
        }

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert "user" in response.data
        assert "token" in response.data
        assert "refresh" in response.data
        assert response.data["user"]["email"] == "newuser@example.com"
        assert User.objects.filter(email="newuser@example.com").exists()

    def test_register_user_password_mismatch(self, api_client):
        """Test registration with mismatched passwords"""
        url = reverse("register")
        data = {
            "email": "test@example.com",
            "password": "SecurePass123!",
            "password2": "DifferentPass123!",
            "first_name": "Test",
            "last_name": "User",
        }

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert not User.objects.filter(email="test@example.com").exists()

    def test_register_user_duplicate_email(self, api_client, user):
        """Test registration with duplicate email"""
        url = reverse("register")
        data = {
            "email": user.email,
            "password": "SecurePass123!",
            "password2": "SecurePass123!",
            "first_name": "Test",
            "last_name": "User",
        }

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_user_weak_password(self, api_client):
        """Test registration with weak password"""
        url = reverse("register")
        data = {
            "email": "weak@example.com",
            "password": "123",
            "password2": "123",
            "first_name": "Test",
            "last_name": "User",
        }

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert not User.objects.filter(email="weak@example.com").exists()

    def test_register_user_missing_fields(self, api_client):
        """Test registration with missing required fields"""
        url = reverse("register")
        data = {"email": "incomplete@example.com", "password": "SecurePass123!"}

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.auth
@pytest.mark.integration
class TestUserLogin:
    """Test user login"""

    def test_login_success(self, api_client, user):
        """Test successful login"""
        url = reverse("login")
        data = {"email": "john@example.com", "password": "TestPass123!"}

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert "token" in response.data
        assert "refresh" in response.data
        assert "user" in response.data
        assert response.data["user"]["email"] == user.email

    def test_login_invalid_credentials(self, api_client, user):
        """Test login with invalid credentials"""
        url = reverse("login")
        data = {"email": user.email, "password": "WrongPassword123!"}

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_nonexistent_user(self, api_client):
        """Test login with non-existent user"""
        url = reverse("login")
        data = {"email": "nonexistent@example.com", "password": "SomePassword123!"}

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_missing_fields(self, api_client):
        """Test login with missing fields"""
        url = reverse("login")
        data = {"email": "test@example.com"}

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.auth
@pytest.mark.integration
class TestUserProfile:
    """Test user profile endpoints"""

    def test_get_profile_authenticated(self, authenticated_client, user):
        """Test getting user profile when authenticated"""
        url = reverse("user-profile")

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["email"] == user.email
        assert response.data["first_name"] == user.first_name
        assert response.data["last_name"] == user.last_name

    def test_get_profile_unauthenticated(self, api_client):
        """Test getting profile without authentication"""
        url = reverse("user-profile")

        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_profile_authenticated(self, authenticated_client, user):
        """Test updating user profile"""
        url = reverse("user-profile")
        data = {"first_name": "Updated", "last_name": "Name"}

        response = authenticated_client.patch(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["first_name"] == "Updated"
        assert response.data["last_name"] == "Name"

        user.refresh_from_db()
        assert user.first_name == "Updated"
        assert user.last_name == "Name"

    def test_update_profile_email_not_allowed(self, authenticated_client, user):
        """Test that email cannot be updated"""
        url = reverse("user-profile")
        original_email = user.email
        data = {"email": "newemail@example.com"}

        response = authenticated_client.patch(url, data, format="json")

        user.refresh_from_db()
        assert user.email == original_email


@pytest.mark.auth
@pytest.mark.integration
class TestTokenRefresh:
    """Test token refresh functionality"""

    def test_token_refresh_success(self, api_client, user):
        """Test successful token refresh"""
        from rest_framework_simplejwt.tokens import RefreshToken

        refresh = RefreshToken.for_user(user)
        url = reverse("token-refresh")
        data = {"refresh": str(refresh)}

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data

    def test_token_refresh_invalid_token(self, api_client):
        """Test token refresh with invalid token"""
        url = reverse("token-refresh")
        data = {"refresh": "invalid-token-string"}

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
