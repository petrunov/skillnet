# accounts/urls.py

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegistrationView,
    ActivationView,
    CustomTokenObtainPairView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    LogoutView,
)

urlpatterns = [
    # 1. User registration & email activation
    path('register/', RegistrationView.as_view(), name='account-register'),
    path('activate/<int:uid>/<str:token>/', ActivationView.as_view(), name='account-activate'),

    # 2. Login and token refresh (JWT)
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 3. Password reset
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('password-reset-confirm/<int:uid>/<str:token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    # 4. Logout (optional, e.g. blacklist refresh token)
    path('logout/', LogoutView.as_view(), name='account-logout'),
]
