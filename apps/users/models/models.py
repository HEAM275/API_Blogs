from django.db import models
from django.contrib.auth.models import AbstractUser
from core.models import AuditableMixins
from ..validators import *

# Create your models here.


class User(AuditableMixins, AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_writer = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def clean(self):
        super().clean()
        # Validar formato del email
        validate_email_address(self.email)

        # Validar contraseña (si se está creando o actualizando)
        if self.pk is None or (hasattr(self, '_password') and self._password != self.password):
            validate_password_strength(self.password, self.username)
