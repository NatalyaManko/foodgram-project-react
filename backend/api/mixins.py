from rest_framework import mixins
#from rest_framework.exceptions import MethodNotAllowed
from rest_framework.viewsets import GenericViewSet


class ListRetriveMixin(mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       GenericViewSet
                       ):
    
    pass
