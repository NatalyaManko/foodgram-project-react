from api.permissions import IsAuthorPermission
from django.core.exceptions import ObjectDoesNotExist
from djoser.views import UserViewSet
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from .models import Follow, User
from .serializers import (FollowSerializer,
                          PasswordChangeSerializer,
                          UserCreateSerializer,
                          UserSerializer)


class CustomUserViewSet(UserViewSet):
    """ViewSet пользователя"""
    queryset = User.objects.all()
    pagination_class = LimitOffsetPagination
    permission_classes = (permissions.AllowAny,
                          IsAuthorPermission,
                          )

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return UserSerializer
        return UserCreateSerializer

    @action(
        methods=['get'],
        detail=False,
        url_path='me',
        permission_classes=[permissions.IsAuthenticated],
        pagination_class=None
    )
    def current_me(self, request):
        """Просмотр страницы текущего пользователя"""
        serializer = UserSerializer(request.user,)
        return Response(serializer.data, status.HTTP_200_OK)

    @action(
        methods=['post'],
        detail=False,
        url_path='set_password',
        permission_classes=[permissions.IsAuthenticated,],
        pagination_class=None
    )
    def password_change(self, request):
        """Смена пароля"""
        serializer = PasswordChangeSerializer(
            request.user,
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            self.request.user.set_password(serializer.data['new_password'])
            self.request.user.save()
            return Response(
                {'Пароль успешно изменен!'},
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

    @action(
        methods=['post', 'delete'],
        detail=True,
        url_path='subscribe',
        permission_classes=[permissions.IsAuthenticated],
        pagination_class=None
    )
    def subscribe(self, request, *args, **kwargs):
        """Создание и удаление подписки"""
        try:
            following = User.objects.get(id=self.kwargs.get('id'))
        except ObjectDoesNotExist:
            return Response({'errors': 'Объект не найден!'},
                            status=status.HTTP_404_NOT_FOUND)
        follower = self.request.user
        if request.method == 'POST':
            serializer = FollowSerializer(
                data=request.data,
                context={'request': request, 'following': following}
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save(following=following, follower=follower)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
        if Follow.objects.filter(following=following,
                                 follower=follower).exists():
            Follow.objects.get(following=following).delete()
            return Response('Успешная отписка',
                            status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {'errors': 'Вы не подписаны на этого пользователя!'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(
        methods=['get'],
        detail=False,
        url_path='subscriptions',
        permission_classes=[permissions.IsAuthenticated]
    )
    def current_subscriptions(self, request):
        """Просмотр страницы подписок"""
        follows = Follow.objects.filter(follower=self.request.user)
        pages = self.paginate_queryset(follows)
        serializer = FollowSerializer(pages,
                                      many=True,
                                      context={'request': request})
        return self.get_paginated_response(serializer.data)
