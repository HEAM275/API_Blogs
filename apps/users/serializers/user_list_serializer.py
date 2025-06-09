from rest_framework import serializers
from apps.core.serializers.base_serializer import AuditableSerializerMixin
from apps.users.models import User


class UserListSerializer(AuditableSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_writer',
            'created_date',
            'created_by',
            'updated_date',
            'updated_by',
            'deleted_date',
            'deleted_by'
        ]
        read_only_fields = fields
