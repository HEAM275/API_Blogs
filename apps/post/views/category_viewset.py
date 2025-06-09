from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from apps.core.views.base_viewset import BaseModelViewSet
from apps.post.models.categoria import Categoria
from apps.post.serializers.category_serializers import CategoriaListSerializer, CategoriaCreateUpdateSerializer


class CategoriaViewSet(BaseModelViewSet):
    queryset = Categoria.objects.filter(is_active=True)
    serializer_class = CategoriaListSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CategoriaCreateUpdateSerializer

    @swagger_auto_schema(
        operation_description="Lista todas las categorías",
        responses={
            200: CategoriaListSerializer(many=True),
            403: "No tienes permiso para realizar esta acción"
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Obtiene detalles de una categoría específica",
        responses={
            200: CategoriaListSerializer(),
            404: "Categoría no encontrada",
            403: "No tienes permiso para realizar esta acción"
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Crea una nueva categoría",
        request_body=CategoriaCreateUpdateSerializer,
        responses={
            201: "Categoría creada exitosamente",
            400: "Datos inválidos",
            403: "No tienes permiso para realizar esta acción"
        }
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Categoría creada exitosamente", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {"message": "Error al crear la categoría", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    @swagger_auto_schema(
        operation_description="Actualiza una categoría existente",
        request_body=CategoriaCreateUpdateSerializer,
        responses={
            200: "Categoría actualizada exitosamente",
            400: "Datos inválidos",
            403: "No tienes permiso para realizar esta acción",
            404: "Categoría no encontrada"
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
                {"message": "Categoría actualizada exitosamente",
                    "data": serializer.data},
                status=status.HTTP_200_OK
            )
        return Response(
            {"message": "Error al actualizar la categoría",
                "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    @swagger_auto_schema(
        operation_description="Elimina una categoría",
        responses={
            204: "Categoría eliminada exitosamente",
            403: "No tienes permiso para realizar esta acción",
            404: "Categoría no encontrada"
        }
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Categoría eliminada exitosamente"},
            status=status.HTTP_204_NO_CONTENT
        )
