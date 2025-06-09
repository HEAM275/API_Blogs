from rest_framework import serializers
from apps.post.models.post import Post
from apps.post.models.contenido_multimedia import ContenidoMultimedia
from apps.post.models.categoria import Categoria
from apps.users.models import User
from apps.post.serializers.cont_mult_serializer import MultimediaListSerializer


class AutorInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class PostListSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    autor = AutorInfoSerializer(read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'titulo',
            'category',
            'summary',
            'description',
            'fecha_publicacion',
            'autor'
        ]


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(),
        source='category'
    )

    class Meta:
        model = Post
        fields = [
            'titulo',
            'category',
            'summary',
            'description',
            'contenido',
            'estado',
            'fecha_publicacion',
            'palabras_clave',
            'imagen_portada',
        ]

    def validate_titulo(self, value):
        if len(value) < 10:
            raise serializers.ValidationError(
                "El título debe tener al menos 10 caracteres.")
        return value

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['autor'] = request.user
        return super().create(validated_data)


class PostDetailSerializer(PostListSerializer):
    multimedia = MultimediaListSerializer(many=True, read_only=True)
    imagen_portada_url = serializers.SerializerMethodField()

    class Meta(PostListSerializer.Meta):
        fields = PostListSerializer.Meta.fields + [
            'contenido',
            'estado',
            'palabras_clave',
            'imagen_portada',
            'imagen_portada_url',
            'multimedia',
            'slug',
            'created_at',
            'updated_at'
        ]

    def get_imagen_portada_url(self, obj):
        request = self.context.get('request')
        if obj.imagen_portada and hasattr(obj.imagen_portada, 'url'):
            return request.build_absolute_uri(obj.imagen_portada.url)
        return None
