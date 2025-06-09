from rest_framework import serializers
from apps.users.serializers.user_list_serializer import UserListSerializer


class PerfilSerializer(UserListSerializer):
    class Meta(UserListSerializer.Meta):
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id', 'username', 'email']
