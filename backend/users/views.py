from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from subscriptions.models import Subscription
from subscriptions.serializers import SubscriptionSerializer
from users.serializers import (PasswordSerializer,
                               UserCreateSerializer,
                               UserSerializer)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint для пользователей.
    """

    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        """
        Получить класс сериализатора в зависимости от типа запроса.
        Возвращает:
            Класс сериализатора.
        """
        if self.request.method in ('POST',):
            return UserCreateSerializer
        return UserSerializer

    @action(('get',), detail=False, permission_classes=(IsAuthenticated,))
    def me(self, request):
        """
        Получение информации о текущем пользователе.
        """
        return Response(UserSerializer(request.user).data,
                        status=status.HTTP_200_OK)

    @action(('post',), detail=False, permission_classes=(IsAuthenticated,))
    def set_password(self, request, *args, **kwargs):
        """
        Установка нового пароля для текущего пользователя.
        """
        serializer = PasswordSerializer(data=request.data,
                                        context={"request": self.request})
        serializer.is_valid(raise_exception=True)

        self.request.user.password = serializer.validated_data['new_password']
        self.request.user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(('post', 'delete'), detail=True,
            permission_classes=(IsAuthenticated,))
    def subscribe(self, request, *args, **kwargs):
        """
        Подписка или отписка текущего пользователя на другого пользователя.
        """
        author = get_object_or_404(User, id=kwargs['pk'])
        user = request.user

        if request.method == 'POST':
            subscription = Subscription(user=user, author=author)
            serializer = SubscriptionSerializer(
                subscription, context={'request': request}
            )
            subscription.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            subscription = Subscription.objects.get(user=user, author=author)
            subscription.delete()
            return Response(
                {'detail': 'OK'}, status=status.HTTP_204_NO_CONTENT
            )
