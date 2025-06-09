from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import PermissionDenied
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django_filters.rest_framework import DjangoFilterBackend
from apps.core.views.base_viewset import BaseModelViewSet
from apps.post.models.post import Post
from apps.post.serializers.post_serializer import (
    PostListSerializer,
    PostDetailSerializer,
    PostCreateUpdateSerializer
)
from apps.post.filters import PostFilter
from apps.post.pagination import StandardResultsSetPagination
from apps.post.permissions import IsWriter


class PostViewSet(BaseModelViewSet):
    serializer_class = PostListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = PostFilter

    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:
            return Post.objects.none()

        # Admin puede ver todo
        if user.is_superuser or user.is_staff:
            return Post.objects.all().select_related('autor', 'category')

        # Escritor solo ve sus artículos
        if user.is_writer:
            return Post.objects.filter(autor=user, is_active=True).select_related('autor', 'category')

        # Usuario común solo ve artículos publicados
        return Post.objects.filter(estado='publicado', is_active=True).select_related('autor', 'category')

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsWriter, IsAdminUser]
        elif self.action in ['list', 'retrieve']:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def perform_update(self, serializer):
        post = serializer.save()
        if post.autor != self.request.user and not self.request.user.is_superuser:
            raise PermissionDenied(
                "No puedes editar artículos que no son tuyos.")

    def perform_destroy(self, instance):
        if instance.autor != self.request.user and not self.request.user.is_superuser:
            raise PermissionDenied(
                "No puedes eliminar artículos que no son tuyos.")

    @swagger_auto_schema(
        operation_description="Lista todos los artículos con opciones de filtrado",
        manual_parameters=[
            openapi.Parameter('autor_nombre', openapi.IN_QUERY,
                              description="Buscar por nombre o apellido del autor", type=openapi.TYPE_STRING),
            openapi.Parameter('fecha_publicacion', openapi.IN_QUERY,
                              description="Buscar por fecha de publicación (YYYY-MM-DD)", type=openapi.TYPE_STRING),
            openapi.Parameter('categoria', openapi.IN_QUERY,
                              description="Buscar por ID de categoría", type=openapi.TYPE_INTEGER),
            openapi.Parameter('page', openapi.IN_QUERY,
                              description="Número de página", type=openapi.TYPE_INTEGER),
            openapi.Parameter('page_size', openapi.IN_QUERY,
                              description="Tamaño de página", type=openapi.TYPE_INTEGER),
        ],
        responses={
            200: openapi.Response("Respuesta paginada", PostListSerializer(many=True)),
            403: "No tienes permiso para realizar esta acción"
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Obtiene detalles de un artículo específico",
        responses={
            200: PostDetailSerializer(),
            404: "Artículo no encontrado",
            403: "No tienes permiso para realizar esta acción"
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Crea un nuevo artículo asignando automáticamente al autor actual",
        request_body=PostCreateUpdateSerializer,
        responses={
            201: "Artículo creado exitosamente",
            400: "Datos de entrada inválidos",
            403: "No tienes permiso para realizar esta acción"
        }
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Artículo creado exitosamente", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {"message": "Error en la creación", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    @swagger_auto_schema(
        operation_description="Actualiza un artículo existente",
        request_body=PostCreateUpdateSerializer,
        responses={
            200: "Artículo actualizado exitosamente",
            400: "Datos de entrada inválidos",
            403: "No tienes permiso para realizar esta acción",
            404: "Artículo no encontrado"
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
                {"message": "Artículo actualizado exitosamente",
                    "data": serializer.data},
                status=status.HTTP_200_OK
            )
        return Response(
            {"message": "Error en la actualización", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    @swagger_auto_schema(
        operation_description="Elimina lógicamente un artículo (cambia estado a archivado)",
        responses={
            204: "Artículo archivado exitosamente",
            403: "No tienes permiso para realizar esta acción",
            404: "Artículo no encontrado"
        }
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.estado = 'archivado'
        instance.is_active = False
        instance.save()
        return Response(
            {"message": "Artículo archivado exitosamente"},
            status=status.HTTP_204_NO_CONTENT
        )

    @swagger_auto_schema(
        operation_description="Reactiva un artículo previamente archivado",
        responses={
            200: "Artículo reactivado exitosamente",
            400: "El artículo ya está activo o no se puede reactivar",
            403: "No tienes permiso para realizar esta acción",
            404: "Artículo no encontrado"
        }
    )
    @action(detail=True, methods=['post'], permission_classes=[IsWriter])
    def reactivate(self, request, pk=None):
        post = self.get_object()
        if post.estado != 'archivado':
            return Response(
                {"message": "El artículo no está archivado"},
                status=status.HTTP_400_BAD_REQUEST
            )
        post.estado = 'publicado'
        post.save()
        serializer = self.get_serializer(post)
        return Response(
            {"message": "Artículo reactivado exitosamente", "data": serializer.data},
            status=status.HTTP_200_OK
        )
