import csv
from django.shortcuts import render
from rest_framework import viewsets, filters, status, permissions
from django_filters.rest_framework import DjangoFilterBackend
#from rest_framework. import IsAuthenticationOrReadOnly, IsAdminUser
from rest_framework.throttling import AnonRateThrottle
from rest_framework.decorators import action
from rest_framework.response import Response
from recipes.models import (Recipe, Tag, Ingredient,
                            RecipeIngredient,
                            ShoppingCart,
                            Favorite)
from django.db.models import Sum
from django.http import HttpResponse
from .serializers import (RecipeGetSerializer,
                          RecipeCreateSerializer,
                          TagSerializer,
                          IngredientSerializer,
                          ShoppingCartSerializer,
                          FavoriteSerializer)
from .filters import TagFilter, RecipeFilter
from .permissions import (IsAuthorPermission)
from rest_framework.exceptions import PermissionDenied, ValidationError

from rest_framework.pagination import LimitOffsetPagination


class TagListRetrieve(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = None
    filter_backend = (filters.SearchFilter,)
    filterset_class = TagFilter
    search_fields = ('name',)


class IngredientListRetrieve(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = None
    filter_backend = (filters.OrderingFilter)
    ordering_fields = ('name',)
    
    def get_queryset(self):
        queryset = Ingredient.objects.all()
        name_query = self.request.query_params.get('name', None)
        if name_query:
            queryset = queryset.filter(name__startswith=name_query)
        return queryset


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAuthorPermission)
    pagination_class = LimitOffsetPagination
    throttle_classes = (AnonRateThrottle,)
    throttle_scope = 'travel_speed'
    filter_backend = (DjangoFilterBackend,
                      filters.OrderingFilter)
    filterset_class = RecipeFilter
    ordering_fields = ('-id',)
    
    def get_serializer_class(self):
        if self.action ==('list', 'retrieve'):
            return RecipeGetSerializer
        return RecipeCreateSerializer

    def perform_update(self, serializer, **kwargs):
        recipe = self.get_object()
        if recipe.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super().perform_update(serializer, **kwargs)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('У вас нет прав для удаления этого рецепта!')
        instance.delete()
        return Response('Успешное удаление!', status=status.HTTP_204_NO_CONTENT)


class ShoppingCartViewSet(viewsets.ModelViewSet):
    
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class=None

    @action(methods=['post'],
            detail=True)
    def add_recipe_to_cart(self, request, pk=None):
        """
        Добавляет рецепт в список покупок текущего пользователя.
        """
        recipe = Recipe.objects.get(pk=pk)
        if recipe:
            ShoppingCart.objects.create(user=request.user, recipe=recipe)
            return Response({"message": "Рецепт успешно добавлен в список покупок."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Рецепт не найден."}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['post'],
            detail=True)
    def remove_recipe_from_cart(self, request, pk=None):
        """
        Удаляет рецепт из списка покупок текущего пользователя.
        """
        try:
            shopping_cart_item = ShoppingCart.objects.get(pk=pk, user=request.user)
            shopping_cart_item.delete()
            return Response({'error': 'Рецепт успешно удален из списка покупок!'},
                            status=status.HTTP_204_NO_CONTENT)
        except ShoppingCart.DoesNotExist:
            return Response({"error": "Запись не найдена!"}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['get'],
            detail=False,
            url_path='download_shopping_cart')
    def export_shopping_cart(self, request):
        """Отправка csv-файла со списком покупок"""
        shopping_cart_items = RecipeIngredient.objects.filter(
            recipe__shopping_cart__user=self.request.user
        ).prefetch_related(
            'recipe__shopping_cart', 'user', 'ingredient'
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(
            ingredient_amount=Sum('amount')
        )
        
        shopping_cart = [
            {
                'Название': item['ingredient__name'],
                'Единица измерения': item['ingredient__measurement_unit'],
                'Количество': item['ingredient_amount'],
            }
            for item in shopping_cart_items
        ]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = (
            'attachment; filename="shopping_cart.csv"'
        )
        response.write(u'\ufeff'.encode('utf-8'))
        
        writer = csv.DictWriter(
            response, fieldnames=[
                'Название', 'Единица измерения', 'Количество'
            ]
        )
        writer.writeheader()
        writer.writerows(shopping_cart)

        return response


class FavoriteViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Favorite."""

    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class=None

    @action(methods=['post'],
            detail=True)
    def add_recipe_to_cart(self, request, pk=None):
        """
        Добавляет рецепт в избранное текущего пользователя.
        """
        recipe = Recipe.objects.get(pk=pk)
        if recipe:
            Favorite.objects.create(user=request.user, recipe=recipe)
            return Response({"error": "Рецепт успешно добавлен в избранное!"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Рецепт не найден."}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['delete'],
            detail=True)
    def remove_recipe_from_cart(self, request, pk=None):
        """
        Удаляет рецепт из избранного текущего пользователя.
        """
        try:
            favorite_item = Favorite.objects.get(pk=pk, user=request.user)
            favorite_item.delete()
            return Response({"error": "Рецепт успешно удален из избранного."}, status=status.HTTP_204_NO_CONTENT)
        except Favorite.DoesNotExist:
            return Response({"error": "Запись не найдена."}, status=status.HTTP_404_NOT_FOUND)
