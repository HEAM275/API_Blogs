# apps/blog/views/base_viewset.py

from rest_framework import viewsets, status
from rest_framework.response import Response
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
        instance.is_active = False  # o usa is_active=False si aplica
        instance.save()
