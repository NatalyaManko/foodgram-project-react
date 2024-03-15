from django.core.exceptions import ObjectDoesNotExist
from djoser.views import UserViewSet
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


from .models import Follow, User
from .serializers import (FollowSerializer,
                          UserCreateSerializer,
                          UserSerializer)
from api.permissions import IsAuthorPermission


class CustomUserViewSet(UserViewSet):
    """ViewSet пользователя"""
    queryset = User.objects.all()
    pagination_class = LimitOffsetPagination
    permission_classes = (permissions.AllowAny,)

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
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status.HTTP_200_OK)

    @action(
        methods=['post'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
        pagination_class=None
    )
    def set_password(self, request):
        return UserViewSet.as_view({"post": "set_password"})(request._request)

    def create(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated, IsAuthorPermission,)
    pagination_class=None

    @action(
        methods=['post', 'delete'],
        detail=True,
    )
    def subscribe(self, request, **kwargs):
        """Создание и удаление подписки"""
        breakpoint()        
        follower = request.user
        try:
            following = User.objects.get(id=self.kwargs.get('pk'))
        except ObjectDoesNotExist:
            return Response({'errors': 'Объект не найден!'},
                            status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':
            if Follow.objects.filter(follower=follower, following=following).exists():
                return Response({'errors': 'Вы уже подписаны!'},
                                status=status.HTTP_400_BAD_REQUEST)
            serializer = FollowSerializer(
                data=request.data,
                context={'request': request, 'following': following}
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save(follower=follower, following=following)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            try:
                subscription = Follow.objects.get(follower=follower, following=following)
                subscription.delete()
                return Response({'detail': 'Успешная отписка'}, status=status.HTTP_204_NO_CONTENT)
            except Follow.DoesNotExist:
                return Response({'errors': 'Подписка не существует'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(
        methods=['get'],
        detail=False,
        url_path='subscriptions',
        permission_classes=[permissions.IsAuthenticated]
    )
    def current_subscriptions(self, request):
        """Просмотр страницы подписок"""
        subscriptions = Follow.objects.filter(follower=request.user)
        serializer = FollowSerializer(subscriptions, many=True, context={'request': request})
        return Response(serializer.data)