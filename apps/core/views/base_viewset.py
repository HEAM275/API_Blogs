from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone


def get_user_fullname(user):
    full_name = f"{user.first_name} {user.last_name}".strip()
    return full_name or user.username


class BaseModelViewSet(viewsets.ModelViewSet):
    def perform_create(self, serializer):
        request = self.request
        user = request.user
        full_name = get_user_fullname(user)
        serializer.save(
            created_by=full_name,
            created_date=timezone.now()
        )

    def perform_update(self, serializer):
        request = self.request
        user = request.user
        full_name = get_user_fullname(user)
        serializer.save(
            updated_by=full_name,
            updated_date=timezone.now()
        )

    def perform_destroy(self, instance):
        user = self.request.user
        full_name = get_user_fullname(user)
        instance.deleted_by = full_name
        instance.deleted_date = timezone.now()
        if hasattr(instance, 'estado'):
            instance.estado = 'archivado'
        elif hasattr(instance, 'is_active'):
            instance.is_active = False
        instance.save()
