from rest_framework.pagination import LimitOffsetPagination


class SubscriptionPagination(LimitOffsetPagination):
    default_limit = 10
    limit_query_param = 'limit'
