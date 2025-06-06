from rest_framework import serializers
from django.contrib.auth.hashers import check_password, make_password
from ..models.models import User
from ..validators import validate_email_address, validate_password_strength


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'is_writer')
        read_only_fields = fields  # Todos son de solo lectura


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'is_writer', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
            # Validación automática
            'email': {'validators': [validate_email_address]}
        }

    def validate(self, data):
        # Validar fortaleza de la contraseña (opcional: añade el username si necesitas)
        if 'password' in data:
            validate_password_strength(
                data['password'], data.get('username', ''))
        return data

    def create(self, validated_data):
        # Encriptar la contraseña al crear el usuario
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class UserUpdateSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=False)
    new_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'is_writer',
                  'old_password', 'new_password')
        read_only_fields = ('username', 'email')  # Campos no editables

    def validate(self, data):
        # Validar email si se incluyó en la solicitud
        if 'email' in data:
            validate_email_address(data['email'])

        # Validar contraseña (solo si se envía new_password)
        if 'new_password' in data:
            if 'old_password' not in data:
                raise serializers.ValidationError(
                    {"old_password": "Debes proporcionar tu contraseña actual."}
                )

            if not check_password(data['old_password'], self.instance.password):
                raise serializers.ValidationError(
                    {"old_password": "Contraseña actual incorrecta."}
                )

            if check_password(data['new_password'], self.instance.password):
                raise serializers.ValidationError(
                    {"new_password": "La nueva contraseña no puede ser igual a la anterior."}
                )

            # Validar fortaleza de la nueva contraseña
            validate_password_strength(
                data['new_password'], self.instance.username)

        return data

    def update(self, instance, validated_data):
        # Actualizar campos normales
        instance.first_name = validated_data.get(
            'first_name', instance.first_name)
        instance.last_name = validated_data.get(
            'last_name', instance.last_name)
        instance.is_writer = validated_data.get(
            'is_writer', instance.is_writer)

        # Actualizar contraseña si se proporcionó
        if 'new_password' in validated_data:
            instance.set_password(validated_data['new_password'])

        instance.save()
        return instance
