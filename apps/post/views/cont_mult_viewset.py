from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from apps.post.models.contenido_multimedia import ContenidoMultimedia
from apps.post.serializers.cont_mult_serializer import MultimediaListSerializer, MultimediaCreateUpdateSerializer


class ContenidoMultimediaViewSet(viewsets.ModelViewSet):
    queryset = ContenidoMultimedia.objects.all()
    serializer_class = MultimediaListSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return MultimediaCreateUpdateSerializer

    @swagger_auto_schema(
        operation_description="Lista todos los contenidos multimedia",
        responses={
            200: MultimediaListSerializer(many=True),
            403: "No tienes permiso para realizar esta acción"
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Obtiene detalles de un contenido multimedia específico",
        responses={
            200: MultimediaListSerializer(),
            404: "Contenido no encontrado",
            403: "No tienes permiso para realizar esta acción"
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Crea un nuevo contenido multimedia",
        request_body=MultimediaCreateUpdateSerializer,
        responses={
            201: "Contenido creado exitosamente",
            400: "Datos inválidos",
            403: "No tienes permiso para realizar esta acción"
        }
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Contenido multimedia creado exitosamente",
                    "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {"message": "Error al crear el contenido", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    @swagger_auto_schema(
        operation_description="Actualiza un contenido multimedia existente",
        request_body=MultimediaCreateUpdateSerializer,
        responses={
            200: "Contenido actualizado exitosamente",
            400: "Datos inválidos",
            403: "No tienes permiso para realizar esta acción",
            404: "Contenido no encontrado"
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
                {"message": "Contenido actualizado exitosamente",
                    "data": serializer.data},
                status=status.HTTP_200_OK
            )
        return Response(
            {"message": "Error al actualizar el contenido",
                "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    @swagger_auto_schema(
        operation_description="Elimina un contenido multimedia",
        responses={
            204: "Contenido eliminado exitosamente",
            403: "No tienes permiso para realizar esta acción",
            404: "Contenido no encontrado"
        }
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Contenido multimedia eliminado exitosamente"},
            status=status.HTTP_204_NO_CONTENT
        )
