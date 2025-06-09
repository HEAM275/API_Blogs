from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.users.views.user_viewset import UserViewSet

from apps.users.views.perfil_view import (
    PerfilView,
    PerfilUpdateView,
    CambiarPasswordView
)

# Crear el router y registrar el ViewSet
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

# Esto genera automáticamente:
# - GET      /api/users/
# - POST     /api/users/
# - GET      /api/users/{id}/
# - PUT      /api/users/{id}/
# - PATCH    /api/users/{id}/
# - DELETE   /api/users/{id}/
# - POST     /api/users/{id}/activate/

urlpatterns = [
    path('', include(router.urls)),
    path('perfil/', PerfilView.as_view(), name='perfil'),
    path('perfil/update/', PerfilUpdateView.as_view(), name='perfil-update'),
    path('perfil/change-password/',
         CambiarPasswordView.as_view(), name='change-password'),
]
