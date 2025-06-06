# apps/users/views.py
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..models.models import User
from ..serializers.serializer import (
    UserListSerializer,
    UserCreateSerializer,
    UserUpdateSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserListSerializer

    @swagger_auto_schema(
        operation_description="Lista todos los usuarios activos",
        responses={
            200: UserListSerializer(many=True),
            403: "No tienes permiso para realizar esta acción"
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Obtiene un usuario activo específico",
        responses={
            200: UserListSerializer(),
            404: "Usuario no encontrado",
            403: "No tienes permiso para realizar esta acción"
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Crea un nuevo usuario",
        request_body=UserCreateSerializer,
        responses={
            201: "Usuario creado exitosamente",
            400: "Datos de entrada inválidos",
            403: "No tienes permiso para realizar esta acción"
        }
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Usuario creado exitosamente", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {"message": "Error en la creación", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    @swagger_auto_schema(
        operation_description="Actualiza un usuario existente",
        request_body=UserUpdateSerializer,
        responses={
            200: "Usuario actualizado exitosamente",
            400: "Datos de entrada inválidos",
            403: "No tienes permiso para realizar esta acción",
            404: "Usuario no encontrado"
        }
    )
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Usuario actualizado exitosamente",
                    "data": serializer.data},
                status=status.HTTP_200_OK
            )
        return Response(
            {"message": "Error en la actualización", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    @swagger_auto_schema(
        operation_description="Eliminación lógica (soft delete) de un usuario",
        responses={
            204: "Usuario desactivado exitosamente",
            403: "No tienes permiso para realizar esta acción",
            404: "Usuario no encontrado"
        }
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(
            {"message": "Usuario desactivado exitosamente"},
            status=status.HTTP_204_NO_CONTENT
        )

    @swagger_auto_schema(
        operation_description="Reactiva un usuario previamente desactivado",
        responses={
            200: "Usuario reactivado exitosamente",
            403: "No tienes permiso para realizar esta acción",
            404: "Usuario no encontrado"
        }
    )
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def activate(self, request, pk=None):
        user = self.get_object()
        if user.is_active:
            return Response(
                {"message": "El usuario ya está activo"},
                status=status.HTTP_400_BAD_REQUEST
            )
        user.is_active = True
        user.save()
        return Response(
            {"message": "Usuario reactivado exitosamente"},
            status=status.HTTP_200_OK
        )
