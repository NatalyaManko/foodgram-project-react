from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from subscriptions.serializers import SubscriptionSerializer


class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.authors.all()
