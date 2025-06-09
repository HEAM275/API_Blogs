from rest_framework import serializers


class AuditableSerializerMixin(serializers.Serializer):
    created_date = serializers.DateTimeField(read_only=True)
    created_by = serializers.CharField(read_only=True)
    updated_date = serializers.DateTimeField(read_only=True)
    updated_by = serializers.CharField(read_only=True)
    deleted_date = serializers.DateTimeField(read_only=True)
    deleted_by = serializers.CharField(read_only=True)
