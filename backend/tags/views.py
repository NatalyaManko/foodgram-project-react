from rest_framework import filters, viewsets

from tags.models import Tag
from tags.serializers import TagSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = (filters.SearchFilter, )
    pagination_class = None
    search_fields = ('^name', )
