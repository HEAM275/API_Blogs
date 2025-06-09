from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils.decorators import method_decorator

# Modelos y serializadores
from apps.users.models import User
from apps.users.serializers.perfil_serializer import PerfilSerializer
from apps.users.serializers.user_create_update_serializer import UserUpdateSerializer
from apps.users.validators import validate_password_strength


# ===== Vista para obtener el perfil =====
@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_description="Obtiene información del usuario autenticado",
    responses={
        200: PerfilSerializer,
        401: "No autenticado"
    }
))
class PerfilView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        usuario = request.user
        serializer = PerfilSerializer(usuario)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ===== Vista para actualizar datos del perfil =====
@method_decorator(name='put', decorator=swagger_auto_schema(
    operation_description="Actualiza toda la información del perfil del usuario autenticado",
    request_body=UserUpdateSerializer,
    responses={
        200: "Datos actualizados exitosamente",
        400: "Datos inválidos",
        401: "No autenticado"
    }
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    operation_description="Actualización parcial del perfil del usuario",
    request_body=UserUpdateSerializer,
    responses={
        200: "Datos actualizados exitosamente",
        400: "Datos inválidos",
        401: "No autenticado"
    }
))
class PerfilUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        usuario = request.user
        serializer = UserUpdateSerializer(instance=usuario, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Datos actualizados exitosamente",
                    "data": serializer.data},
                status=status.HTTP_200_OK
            )
        return Response(
            {"message": "Error en la actualización", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request):
        return self.put(request)


# ===== Vista para cambiar contraseña =====
@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_description="Cambia la contraseña del usuario autenticado",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'old_password': openapi.Schema(type=openapi.TYPE_STRING),
            'new_password': openapi.Schema(type=openapi.TYPE_STRING)
        },
        required=['old_password', 'new_password']
    ),
    responses={
        200: "Contraseña cambiada exitosamente",
        400: "Datos inválidos o contraseñas no coinciden",
        401: "No autenticado"
    }
))
class CambiarPasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not old_password or not new_password:
            raise ValidationError({
                'error': 'Se requieren las contraseñas nueva y actual'
            })

        usuario = request.user

        if not usuario.check_password(old_password):
            raise PermissionDenied("La contraseña actual es incorrecta.")

        if usuario.check_password(new_password):
            raise ValidationError(
                "La nueva contraseña debe ser diferente a la anterior")

        try:
            validate_password_strength(new_password, usuario.username)
        except ValidationError as e:
            raise ValidationError({"password": e.detail}) from e

        usuario.set_password(new_password)
        usuario.save()

        return Response(
            {"message": "Contraseña actualizada exitosamente"},
            status=status.HTTP_200_OK
        )
