from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'},
        help_text='Enter a secure password.'
    )

    class Meta:
        model = User
        fields = (
            'email',
            'password',
            'account_type',
            'full_name',
            'company_name',
        )

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.is_active = False
        user.save()
        return user


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(help_text="Refresh JWT to blacklist")


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(help_text="Email associated with your account")


class PasswordResetConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
        help_text='New password'
    )

    def validate_password(self, value):
        validate_password(value)
        return value
