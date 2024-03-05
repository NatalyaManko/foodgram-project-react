from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from .serializers import (UserSerializer,
                          UserCreateSerializer,
                          PasswordChangeSerializer,
                          FollowSerializer)
from .models import User, Follow
from .paginations import SubscriptionPagination
from api.permissions import IsAuthorPermission, ReadOnly
from .permissions import IsAdminPermission


class CustomUserViewSet(viewsets.ModelViewSet):
    """ViewSet пользователя"""
    queryset = User.objects.all()
    pagination_class = SubscriptionPagination
    permission_classes = (permissions.IsAuthenticated,
                          IsAdminPermission,
                          IsAuthorPermission,
                          ReadOnly,)
    
    def get_serializer_class(self):
        if self.action in ('list','retrieve'):
            return UserSerializer
        return UserCreateSerializer
    
    @action(
        methods=['get'],
        detail=False,
        url_path='me',
        permission_classes=[IsAuthorPermission] # npoBepd
    )
    def current_me(self, request):
        """Просмотр страницы текущего пользователя"""
        serializer = UserSerializer(request.user,)
        return Response(serializer.data, status.HTTP_200_OK)
    
    @action(
        methods=['post'],
        detail=False,
        url_path='set_password',
 #       permission_classes=(IsAuthorPermission),
        pagination_class = None
        )
    def password_change(self, request):
        """Смена пароля"""
        serializer = PasswordChangeSerializer(
            request.user,
            data=request.data,
            context={'request': request}
            )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {'Пароль успешно изменен!'},
                status=status.HTTP_204_NO_CONTENT
                )

    @action(
        methods=['post', 'delete'],
        detail=True,
        url_path='subscribe',
        permission_classes = [permissions.IsAuthenticated, IsAuthorPermission],
        pagination_class = None
        )
    def subscribe(self, request, *args, **kwargs):
        """Создание и удаление подписки"""
        try:
            following = User.objects.get(id=self.kwargs.get('pk'))
        except:
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
            return Response({'errors': 'Вы не подписаны на этого пользователя!'},
                                status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=['get'],
        detail=False,
        url_path='subscriptions',
        permission_classes=[IsAuthorPermission] #-||-
        )
    def current_subscriptions(self, request):
        """Просмотр страницы подписок"""
        follows = Follow.objects.filter(follower=self.request.user)
        pages = self.paginate_queryset(follows)
        serializer = FollowSerializer(pages,
                                      many=True,
                                      context={'request': request})
        return self.get_paginated_response(serializer.data)
