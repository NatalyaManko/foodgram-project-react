from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)


class ApiPagination(LimitOffsetPagination):
    default_limit = 5
    limit_query_param = 'limit'


class PagePagination(PageNumberPagination):
    page_size = 10
    