from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from apps.users.models import User


class PromoteToWriterView(APIView):
    permission_classes = [IsAdminUser]  # Solo admins pueden hacer esto

    def post(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        user.is_writer = True
        user.save(update_fields=['is_writer'])

        return Response({
            'message': f'{user.username} ahora tiene permiso de escritor.'
        }, status=status.HTTP_200_OK)
