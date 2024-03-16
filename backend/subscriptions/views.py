from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from subscriptions.serializers import SubscriptionSerializer


class SubscriptionViewSet(viewsets.ModelViewSet):
    """
    API endpoint для управления подписками пользователя.
    """

    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        Получить запрос на подписки пользователя.

        Возвращает:
            QuerySet: Запрос на подписки пользователя.
        """
        return self.request.user.authors.all()
