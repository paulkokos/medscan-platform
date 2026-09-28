"""
Integration tests for authentication endpoints
"""
from unittest.mock import patch

import pytest
from django.test import override_settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.settings import api_settings
from rest_framework.throttling import ScopedRateThrottle

User = get_user_model()


@pytest.fixture(autouse=True)
def isolate_anon_throttle_ident(monkeypatch, request):
    """Give each test a unique anonymous throttle identifier"""
    original_get_ident = ScopedRateThrottle.get_ident
    test_suffix = abs(hash(request.node.nodeid))

    def get_ident(self, request_obj):
        return f"{original_get_ident(self, request_obj)}:{test_suffix}"

    monkeypatch.setattr(ScopedRateThrottle, "get_ident", get_ident)


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

    def test_login_rate_limited_after_repeated_attempts(self, api_client, user):
        """Test login is rate limited after repeated attempts"""
        url = reverse("login")
        data = {"email": user.email, "password": "TestPass123!"}

        with patch.dict(api_settings.DEFAULT_THROTTLE_RATES, {"auth": "2/minute"}):
            first_response = api_client.post(url, data, format="json")
            second_response = api_client.post(url, data, format="json")
            throttled_response = api_client.post(url, data, format="json")

            assert first_response.status_code == status.HTTP_200_OK
            assert second_response.status_code == status.HTTP_200_OK
            assert throttled_response.status_code == status.HTTP_429_TOO_MANY_REQUESTS

    @override_settings(RATE_LIMIT_ENABLED=False)
    def test_login_succeeds_when_rate_limiting_disabled(self, api_client, user):
        """Test login bypasses auth throttling when rate limiting is disabled"""
        url = reverse("login")
        data = {"email": user.email, "password": "TestPass123!"}

        with patch.dict(api_settings.DEFAULT_THROTTLE_RATES, {}, clear=True):
            response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK


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

    def test_token_refresh_rate_limited_after_repeated_requests(self, api_client, user):
        """Test token refresh shares the stricter auth throttle"""
        from rest_framework_simplejwt.tokens import RefreshToken

        refresh = RefreshToken.for_user(user)
        url = reverse("token-refresh")
        data = {"refresh": str(refresh)}

        with patch.dict(api_settings.DEFAULT_THROTTLE_RATES, {"auth": "2/minute"}):
            first_response = api_client.post(url, data, format="json")
            second_response = api_client.post(url, data, format="json")
            throttled_response = api_client.post(url, data, format="json")

            assert first_response.status_code == status.HTTP_200_OK
            assert second_response.status_code == status.HTTP_200_OK
            assert throttled_response.status_code == status.HTTP_429_TOO_MANY_REQUESTS


@pytest.mark.auth
@pytest.mark.integration
class TestUserLogout:
    """Test logout behavior"""

    def test_logout_missing_refresh_token_returns_stable_error(
        self, authenticated_client
    ):
        """Test logout requires a refresh token"""
        url = reverse("logout")

        response = authenticated_client.post(url, {}, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {"error": "Invalid refresh token"}

    def test_logout_invalid_refresh_token_returns_stable_error(
        self, authenticated_client
    ):
        """Test logout does not expose raw token errors"""
        url = reverse("logout")

        response = authenticated_client.post(
            url, {"refresh": "invalid-token-string"}, format="json"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {"error": "Invalid refresh token"}
