"""
Authentication views
"""
import logging

from django.contrib.auth import authenticate, get_user_model
from django.conf import settings
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework_simplejwt.exceptions import TokenBackendError, TokenError
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from .serializers import (
    ChangePasswordSerializer,
    LoginSerializer,
    RegisterSerializer,
    UserSerializer,
)

User = get_user_model()
logger = logging.getLogger(__name__)


class AuthRateLimitMixin:
    """Apply auth throttling only when rate limiting is enabled"""

    throttle_scope = "auth"

    def get_throttles(self):
        throttles = super().get_throttles()

        if settings.RATE_LIMIT_ENABLED:
            return throttles

        return [
            throttle
            for throttle in throttles
            if not isinstance(throttle, ScopedRateThrottle)
        ]


class RegisterView(AuthRateLimitMixin, generics.CreateAPIView):
    """User registration endpoint"""

    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    throttle_classes = (ScopedRateThrottle,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "user": UserSerializer(user).data,
                "token": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(AuthRateLimitMixin, APIView):
    """User login endpoint"""

    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    throttle_classes = (ScopedRateThrottle,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = authenticate(request, username=email, password=password)

        if user is not None:
            if not user.is_active:
                return Response(
                    {"error": "Account is disabled"}, status=status.HTTP_403_FORBIDDEN
                )

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "user": UserSerializer(user).data,
                    "token": str(refresh.access_token),
                    "refresh": str(refresh),
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )


class UserProfileView(generics.RetrieveUpdateAPIView):
    """Get and update user profile"""

    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class ChangePasswordView(AuthRateLimitMixin, APIView):
    """Change user password"""

    permission_classes = (IsAuthenticated,)
    throttle_classes = (ScopedRateThrottle,)

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user

        # Check old password
        if not user.check_password(serializer.validated_data["old_password"]):
            return Response(
                {"error": "Invalid old password"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Set new password
        user.set_password(serializer.validated_data["new_password"])
        user.save()

        return Response(
            {"message": "Password changed successfully"}, status=status.HTTP_200_OK
        )


class LogoutView(AuthRateLimitMixin, APIView):
    """Logout user (invalidate refresh token)"""

    permission_classes = (IsAuthenticated,)
    throttle_classes = (ScopedRateThrottle,)

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()

            return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        except (TokenError, TokenBackendError):
            logger.warning("Logout token invalidation failed")
            return Response(
                {"error": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST
            )


class ThrottledTokenRefreshView(AuthRateLimitMixin, TokenRefreshView):
    """Refresh JWT tokens with the auth throttle applied"""

    permission_classes = (AllowAny,)
    throttle_classes = (ScopedRateThrottle,)
