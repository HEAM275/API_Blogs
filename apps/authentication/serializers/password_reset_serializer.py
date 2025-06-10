from rest_framework import serializers
from apps.users.models import User
from django.core.exceptions import ValidationError


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            self.user = User.objects.get(email=value, is_active=True)
        except User.DoesNotExist:
            raise ValidationError("No se encontró un usuario con este correo.")
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(min_length=8, write_only=True)
    token = serializers.CharField(write_only=True)

    def validate_token(self, value):
        # Aquí validarías el token desde la base o caché
        # Simulación básica:
        if value != "valid-token":
            raise serializers.ValidationError("Token inválido o expirado")
        return value
