from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Serializadores
from apps.authentication.serializers.login_serializer import LoginSerializer
from apps.authentication.serializers.password_reset_serializer import (
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer
)
from apps.authentication.serializers.register_serializer import RegisterSerializer


@swagger_auto_schema(
    operation_description="Inicio de sesión de usuario",
    request_body=LoginSerializer,
    responses={
        200: openapi.Schema(type=openapi.TYPE_OBJECT, properties={
            'token': openapi.Schema(type=openapi.TYPE_STRING),
            'user': openapi.Schema(type=openapi.TYPE_OBJECT, description="Datos del usuario", properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING)
            })
        }),
        400: "Credenciales inválidas"
    }
)
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)

            return Response({
                'token': token.key,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                }
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    # method='post',
    operation_description="Cierra sesión del usuario actual",
    responses={
        204: {"message": "Logout exitoso"}
    }
)
@method_decorator(name='post', decorator=swagger_auto_schema())
class LogoutView(APIView):
    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response({"message": "Logout exitoso"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": "No se pudo cerrar sesión"}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    # method='post',
    operation_description="Solicita un token de recuperación por correo electrónico",
    request_body=PasswordResetRequestSerializer,
    responses={
        200: {"message": "Se ha enviado un token de recuperación"},
        400: "Correo no encontrado"
    }
)
@method_decorator(name='post', decorator=swagger_auto_schema())
class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            # Enviar token vía correo (simulado aquí)
            return Response({
                "message": f"Token de recuperación generado para {user.email}"
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    # method='post',
    operation_description="Cambia la contraseña usando token de recuperación",
    request_body=PasswordResetConfirmSerializer,
    responses={
        200: {"message": "Contraseña actualizada exitosamente"},
        400: "Token o contraseña inválida"
    }
)
@method_decorator(name='post', decorator=swagger_auto_schema())
class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            # Aquí aplicarías el cambio de contraseña
            return Response({"message": "Contraseña actualizada exitosamente"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    operation_description="Registra un nuevo usuario",
    request_body=RegisterSerializer,
    responses={
        201: openapi.Response("Usuario creado exitosamente", RegisterSerializer),
        400: "Datos inválidos"
    }
)
@method_decorator(name='post', decorator=swagger_auto_schema())
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
