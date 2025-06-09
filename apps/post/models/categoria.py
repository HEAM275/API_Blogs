from django.db import models
from apps.core.models import AuditableMixins
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class Categoria(AuditableMixins, models.Model):
    name = models.CharField(
        verbose_name=_('Category name'),
        max_length=100,
        unique=True,
        blank=False,
        null=False
    )
    is_active = models.BooleanField(default=True)

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
