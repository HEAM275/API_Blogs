from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get(
                'request'), username=username, password=password)
            if not user:
                raise serializers.ValidationError(
                    _('Credenciales incorrectas'), code='authorization')
        else:
            raise serializers.ValidationError(
                _('Debe ingresar nombre de usuario y contraseña.'), code='invalid')

        attrs['user'] = user
        return attrs
