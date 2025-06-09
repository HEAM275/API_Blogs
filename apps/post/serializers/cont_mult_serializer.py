from rest_framework import serializers
from apps.post.models.contenido_multimedia import ContenidoMultimedia
from apps.core.serializers.base_serializer import AuditableSerializerMixin


class MultimediaListSerializer(AuditableSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = ContenidoMultimedia
        fields = ['id', 'tipo', 'archivo',
                  'descripcion', 'created_by', 'created_date']
        read_only_fields = fields


class MultimediaCreateUpdateSerializer(MultimediaListSerializer):
    class Meta(MultimediaListSerializer.Meta):
        fields = ['articulo', 'tipo', 'archivo', 'descripcion']

    class Meta:
        model = ContenidoMultimedia
        fields = [
            'id',
            'articulo',
            'archivo',
            'archivo_url',
            'tipo',
            'descripcion',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'archivo_url']

    def get_archivo_url(self, obj):
        request = self.context.get('request')
        if obj.archivo and hasattr(obj.archivo, 'url'):
            return request.build_absolute_uri(obj.archivo.url)
        return None

    def validate_tipo(self, value):
        if value not in dict(ContenidoMultimedia.TIPO_CONTENIDO).keys():
            raise serializers.ValidationError("Tipo de contenido no válido.")
        return value
