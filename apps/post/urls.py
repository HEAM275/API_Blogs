from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.post.views.post_viewset import PostViewSet
from apps.post.views.category_viewset import CategoriaViewSet
from apps.post.views.cont_mult_viewset import ContenidoMultimediaViewSet

# Crear el router y registrar el ViewSet
router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'categorias', CategoriaViewSet, basename='categoria')
router.register(r'multimedia', ContenidoMultimediaViewSet,
                basename='multimedia')

# Las URLs se generan automáticamente:
# - GET      /api/posts/
# - POST     /api/posts/
# - GET      /api/posts/{id}/
# - PUT      /api/posts/{id}/
# - PATCH    /api/posts/{id}/
# - DELETE   /api/posts/{id}/
# - POST     /api/posts/{id}/reactivate/

urlpatterns = [
    path('', include(router.urls)),
]
