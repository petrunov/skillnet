from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from accounts.utils import get_request_language
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from .serializers import (
    RegistrationSerializer,
    LogoutSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    CustomTokenObtainPairSerializer,
)
from django.shortcuts import get_object_or_404
import logging

logger = logging.getLogger('django')

User = get_user_model()

# 1. Registration
class RegistrationView(APIView):
    permission_classes = [permissions.AllowAny]
    renderer_classes = [JSONRenderer]

    @swagger_auto_schema(request_body=RegistrationSerializer)
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(is_active=False)
        token = default_token_generator.make_token(user)
        lang = get_request_language(request)
        activation_link = (
            f"{settings.HOST}"
            f"/{lang}/register/activate/{user.pk}/{token}/"
        )
        try:
            send_mail(
                subject="Activate your account",
                message=f"Click the link to activate your account: {activation_link}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
        except Exception as e:
            logger.error("Registration email failed", exc_info=e)
            raise

        return Response(
            {"code": "registrationSuccessful", "detail": "Registration successful. Check your email to activate your account."},
            status=status.HTTP_201_CREATED
        )

# 2. Activation
class ActivationView(APIView):
    permission_classes = [permissions.AllowAny]
    renderer_classes = [JSONRenderer]

    def get(self, request, uid, token):
        user = get_object_or_404(User, pk=uid)
        if default_token_generator.check_token(user, token):
            if not user.is_active:
                user.is_active = True
                user.save()
            return Response({"code": "accountActivated", "detail": "Account activated."}, status=status.HTTP_200_OK)
        return Response({"code": "invalidOrExpiredToken", "detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

# 3. JWT Login
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        token['account_type'] = user.account_type
        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [permissions.AllowAny]
    renderer_classes = [JSONRenderer]

# 4. Password Reset Request
class PasswordResetRequestView(APIView):
    permission_classes = [permissions.AllowAny]
    renderer_classes = [JSONRenderer]

    @swagger_auto_schema(request_body=PasswordResetRequestSerializer)
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            lang = get_request_language(request)
            reset_link = (
                f"{settings.HOST}"
                f"/{lang}/login/password-reset/confirm/{user.pk}/{token}/"
            )
            try:
                send_mail(
                    subject="Password Reset Request",
                    message=f"Use the following link to reset your password: {reset_link}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=False,
                )
            except Exception as e:
                logger.error("Password reset email failed", exc_info=e)
                raise
        except User.DoesNotExist:
            pass

        return Response(
            {"code": "resetLinkSent", 'detail': 'If an account with that email exists, a reset link has been sent.'},
            status=status.HTTP_200_OK
        )

# 5. Password Reset Confirm
class PasswordResetConfirmView(APIView):
    permission_classes = [permissions.AllowAny]
    renderer_classes = [JSONRenderer]

    @swagger_auto_schema(request_body=PasswordResetConfirmSerializer)
    def post(self, request, uid, token):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = get_object_or_404(User, pk=uid)
        if not default_token_generator.check_token(user, token):
            return Response({"code": "invalidOrExpiredToken", "detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(serializer.validated_data['password'])
        user.save()
        return Response({"code": "passwordResetSuccessfully", "detail": "Password has been reset successfully."}, status=status.HTTP_200_OK)

# 6. Logout
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [JSONRenderer]

    @swagger_auto_schema(
        request_body=LogoutSerializer,
        security=[{'Bearer': []}],
    )
    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            RefreshToken(serializer.validated_data['refresh']).blacklist()
        except Exception:
            return Response({"code": "invalidOrExpiredToken", 'detail': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)
