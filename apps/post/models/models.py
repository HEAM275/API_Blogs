from datetime import timezone
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.urls import reverse
from django.db import models
from django.core.exceptions import ValidationError
from core.models import AuditableMixins
from apps.users.models import User


class Categoria(AuditableMixins, models.Model):
    name = models.CharField(
        verbose_name=_('Category name'),
        max_length=100,
        unique=True,
        blank=False,
        null=False
    )

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['name']

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()

        if not self.name or not self.name.strip():
            raise ValidationError({
                'name': _('The name cannot be empty or just whitespace')
            })

        self.name = self.name.strip().title()


class Post(AuditableMixins, models.Model):
    ESTADOS = (
        ('borrador', _('Borrador')),
        ('publicado', _('Publicado')),
        ('archivado', _('Archivado')),
    )
    autor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='articulos_escritos'
    )
    category = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True,
                                 verbose_name='Categoria del articulo', related_name='articulos')
    titulo = models.CharField(
        verbose_name=_('Título'),
        max_length=200,
        unique=True,
        help_text=_('Título único para el artículo')
    )
    summary = models.TextField(verbose_name=_(
        'Resumen'), null=True, blank=True)
    description = models.CharField(verbose_name=_('Descripcion del articulo'))
    slug = models.SlugField(
        max_length=250,
        unique_for_date='fecha_publicacion',
        allow_unicode=True
    )
    contenido = models.TextField(
        verbose_name=_('Contenido'),
        help_text=_('Formato Markdown recomendado')
    )
    imagen_portada = models.ImageField(
        upload_to='articulos/portadas/%Y/%m/%d/',
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(allowed_extensions=[
                                   'jpg', 'jpeg', 'png', 'webp']),
        ]
    )
    estado = models.CharField(
        max_length=10,
        choices=ESTADOS,
        default='borrador'
    )
    fecha_publicacion = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )
    palabras_clave = models.CharField(
        max_length=250,
        blank=True,
        help_text=_('Palabras separadas por comas')
    )

    class Meta:
        verbose_name = _('Artículo')
        verbose_name_plural = _('Artículos')
        ordering = ['-fecha_publicacion']
        permissions = [
            ('can_publish', 'Puede publicar artículos'),
            ('can_edit_all', 'Puede editar cualquier artículo'),
        ]

    def __str__(self):
        return self.titulo

    def clean(self):
        super().clean()

        if self.estado == 'publicado' and not self.fecha_publicacion:
            self.fecha_publicacion = timezone.now()

        if len(self.titulo) < 10:
            raise ValidationError(
                {'titulo': _('El título debe tener al menos 10 caracteres')}
            )
        if self.imagen_portada:
            # Validar tamaño máximo (ej: 2MB)
            if self.imagen_portada.size > 2 * 1024 * 1024:
                raise ValidationError({
                    'imagen_portada': _('La imagen no puede superar los 2MB')
                })

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo, allow_unicode=True)
        super().save(*args, **kwargs)


class ContenidoMultimedia(models.Model):
    articulo = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='multimedia'
    )
    archivo = models.FileField(upload_to='articulos/media/%Y/%m/%d/')
    tipo = models.CharField(max_length=20, choices=[
                            ('imagen', 'Imagen'), ('video', 'Video')])
    descripcion = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = _('Contenido Multimedia')
