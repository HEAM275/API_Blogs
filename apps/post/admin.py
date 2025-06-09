# apps/post/admin.py
from django.contrib import admin
from apps.post.models.categoria import Categoria
from apps.post.models.post import Post
from apps.post.models.contenido_multimedia import ContenidoMultimedia


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'category',
                    'estado', 'fecha_publicacion')
    list_filter = ('estado', 'category')
    prepopulated_fields = {'slug': ('titulo',)}
    search_fields = ('titulo', 'contenido')


@admin.register(ContenidoMultimedia)
class ContenidoMultimediaAdmin(admin.ModelAdmin):
    list_display = ('articulo', 'tipo', 'descripcion')
