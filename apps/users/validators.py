from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _


def validate_password_strength(password, username):
    """
    validar que:
    - tenga al menos 8 caracteres
    - no contenga el nombre de usuario
    """

    if username.lower() in password.lower():
        raise ValidationError(
            _('La contraseña no puede contener el nombre de usuario'),
            code="password_contain_username")
    if len(password) < 8:
        raise ValidationError(
            _('La contraseña debe tener un mínimo de 8 caracteres'),
            code='password _too_short')


def validate_email_address(email):
    """
    validar que el email sea correcto
    """

    try:
        validate_email(email)
    except:
        raise ValidationError(_(
            'formato de email incorrecto '), code='invalid_email')
