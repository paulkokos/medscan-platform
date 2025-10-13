"""
Authentication URL Configuration
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (ChangePasswordView, LoginView, LogoutView, RegisterView,
                    UserProfileView)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("user/", UserProfileView.as_view(), name="user-profile"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("refresh/", TokenRefreshView.as_view(), name="token-refresh"),
]
