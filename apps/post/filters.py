import django_filters
from django.db.models import Q
from apps.post.models.post import Post


class PostFilter(django_filters.FilterSet):
    autor_nombre = django_filters.CharFilter(
        field_name='autor',
        lookup_expr='icontains',
        method='filter_by_author_name'
    )
    fecha_publicacion = django_filters.DateFilter(
        field_name='fecha_publicacion',
        lookup_expr='date__exact'
    )
    categoria = django_filters.NumberFilter(field_name='category')

    class Meta:
        model = Post
        fields = ['autor_nombre', 'fecha_publicacion', 'categoria']

    def filter_by_author_name(self, queryset, name, value):
        return queryset.filter(
            Q(autor__first_name__icontains=value) |
            Q(autor__last_name__icontains=value)
        )
