from rest_framework import serializers
from apps.core.serializers.base_serializer import AuditableSerializerMixin
from apps.post.models.categoria import Categoria


class CategoriaListSerializer(AuditableSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'name', 'created_date', 'created_by']
        read_only_fields = fields


class CategoriaCreateUpdateSerializer(CategoriaListSerializer):
    class Meta(CategoriaListSerializer.Meta):
        fields = ['name']

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "El nombre no puede estar vacío.")
        return value.title()
