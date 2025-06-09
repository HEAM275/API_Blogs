from django.utils.translation import gettext_lazy as _
from django.db import models
from .post import Post


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
