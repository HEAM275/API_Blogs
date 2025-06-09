from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Modelos y serializadores
from apps.users.models import User
from apps.users.serializers.user_create_update_serializer import UserCreateSerializer, UserUpdateSerializer
from apps.users.serializers.user_list_serializer import UserListSerializer

# Desde core
from apps.core.views.base_viewset import BaseModelViewSet


class UserViewSet(BaseModelViewSet):
    queryset = User.objects.filter(is_active=True)
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserListSerializer

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

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
        operation_description="Obtiene detalles de un usuario específico",
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
            400: "Datos inválidos",
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
        request_body=UserCreateSerializer,
        responses={
            200: "Usuario actualizado exitosamente",
            400: "Datos inválidos",
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
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Reactiva un usuario previamente desactivado",
        responses={
            200: "Usuario reactivado exitosamente",
            400: "El usuario ya está activo o no se puede reactivar",
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
        user.deleted_by = None
        user.deleted_date = None
        user.save()
        return Response(
            {"message": "Usuario reactivado exitosamente",
                "data": UserListSerializer(user).data},
            status=status.HTTP_200_OK
        )
