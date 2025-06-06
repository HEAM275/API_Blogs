from django.db import models

from django.utils.translation import gettext_lazy as _


class AuditableMixins(models.Model):

    created_date = models.DateTimeField(
        verbose_name=_('created date'), auto_now_add=True)
    created_by = models.CharField(verbose_name=_(
        'created by'), max_length=255, null=True, blank=True)

    updated_date = models.DateTimeField(verbose_name=_(
        'updated date'), auto_now_add=False, auto_now=True)
    updated_by = models.CharField(verbose_name=_(
        'updated by'), max_length=255, null=True, blank=True)

    deleted_date = models.DateTimeField(
        verbose_name=_('deleted date'), null=True, blank=True)
    deleted_by = models.CharField(verbose_name=_(
        'deleted by'), max_length=255, null=True, blank=True)

    class Meta:
        abstract = True
