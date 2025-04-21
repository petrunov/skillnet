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
    path('register/', RegistrationView.as_view(), name='account-register'),
    path('activate/<int:uid>/<str:token>/', ActivationView.as_view(), name='account-activate'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('password-reset-confirm/<int:uid>/<str:token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('logout/', LogoutView.as_view(), name='account-logout'),
]
