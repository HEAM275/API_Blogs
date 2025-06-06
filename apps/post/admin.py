from django.contrib import admin
from django.db import models
from django_json_widget.widgets import JSONEditorWidget
from markdownx.widgets import AdminMarkdownxWidget  # Cambio clave aquí

from .models.models import Post


@admin.register(Post)
class ArticuloAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMarkdownxWidget},  # Widget cambiado
    }
    list_display = ['titulo', 'estado', 'autor', 'fecha_publicacion']
    list_filter = ['estado', 'categoria']
    search_fields = ['titulo', 'contenido']
