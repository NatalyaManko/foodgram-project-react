import csv

from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle

from recipes.models import (Favorite,
                            Ingredient,
                            Recipe,
                            RecipeIngredient,
                            ShoppingCart,
                            Tag)

from .filters import IngredientFilter, RecipeFilter, TagFilter
from .permissions import IsAuthorPermission
from .serializers import (FavoriteSerializer,
                          IngredientSerializer,
                          RecipeCreateSerializer,
                          RecipeGetSerializer,
                          ShoppingCartSerializer,
                          TagSerializer)


class TagListRetrieve(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для просмотра списка тегов рецептов.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = None
    filter_backends = (filters.SearchFilter,)
    filterset_class = TagFilter
    search_fields = ('name',)


class IngredientListRetrieve(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для просмотра списка ингредиентов.
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = None
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    filterset_class = IngredientFilter
    search_fields = ('^name',)
    ordering_fields = ('name',)


class RecipeViewSet(viewsets.ModelViewSet):
    """
    ViewSet для создания, просмотра, редактирования и удаления рецептов.
    """
    queryset = Recipe.objects.all()
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorPermission,
    )
    pagination_class = LimitOffsetPagination
    throttle_classes = (AnonRateThrottle,)
    throttle_scope = 'travel_speed'
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    filterset_class = RecipeFilter
    search_fields = ('^name',)
    ordering_fields = ('-id',)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeGetSerializer
        return RecipeCreateSerializer

    def perform_update(self, serializer):
        """
        Переопределенный метод для выполнения обновления рецепта.
        """
        user = self.request.user
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('pk'))
        if recipe.author != user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super().perform_update(serializer)

    def perform_destroy(self, serializer):
        """
        Переопределенный метод для выполнения удаления рецепта.
        """
        user = self.request.user
        try:
            recipe = Recipe.objects.get(id=self.kwargs.get('pk'), author=user)
            recipe.delete()
            return Response('Успешное удаление!',
                            status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            raise PermissionDenied('Изменение чужого контента запрещено!')

    @action(methods=['post', 'delete'],
            detail=True,
            url_path='shopping_cart',
            permission_classes=[permissions.IsAuthenticated,
                                IsAuthorPermission])
    def shopping_cart(self, request, **kwargs):
        """
        Получить / Добавить / Удалить  рецепт из списка покупок.
        """
        user = self.request.user
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('pk'))

        if request.method == 'POST':
            if ShoppingCart.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    {'errors': 'Рецепт уже добавлен в список покупок!'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = ShoppingCartSerializer(
                data=request.data,
                context={'request': request, 'recipe': recipe}
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=user, recipe=recipe)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            if ShoppingCart.objects.filter(user=user, recipe=recipe).exists():
                ShoppingCart.objects.get(recipe=recipe).delete()
                return Response(
                    {'errors': 'Рецепт успешно удален из списка покупок!'},
                    status=status.HTTP_204_NO_CONTENT
                )
            else:
                return Response(
                    {'errors': 'Рецепт не был добавлен в список покупок!'},
                    status=status.HTTP_400_BAD_REQUEST
                )

    @action(methods=['get'],
            detail=False,
            url_path='download_shopping_cart',)
    def export_shopping_cart(self, request):
        """
        Отправка csv-файла со списком покупок.
        """
        shopping_cart_items = (RecipeIngredient.objects.filter(
            recipe__shopping_cart__user=self.request.user).
            prefetch_related('recipe__shopping_cart', 'user', 'ingredient').
            values('ingredient__name', 'ingredient__measurement_unit').
            annotate(ingredient_amount=Sum('amount'))
        )
        shopping_cart = []
        for item in shopping_cart_items:
            shopping_cart.append({
                'Название': item['ingredient__name'],
                'Единица измерения': item['ingredient__measurement_unit'],
                'Количество': item['ingredient_amount'],
            })
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = \
            'attachment; filename="shopping_cart.csv"'
        writer = csv.DictWriter(response,
                                fieldnames=['Название',
                                            'Единица измерения',
                                            'Количество'])
        writer.writeheader()
        writer.writerows(shopping_cart)
        return response

    @action(methods=['post', 'delete'],
            detail=True,
            url_path='favorite',
            permission_classes=[permissions.IsAuthenticated])
    def favourites(self, request, **kwargs):
        """
        Добавить / Удалить  рецепт из избранного.
        """
        user = self.request.user
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('pk'))

        if request.method == 'POST':
            if Favorite.objects.filter(user=user, recipe=recipe).exists():
                return Response({'errors': 'Рецепт уже добавлен в избранное!'},
                                status=status.HTTP_400_BAD_REQUEST)
            serializer = FavoriteSerializer(
                data=request.data,
                context={'request': request, 'recipe': recipe})
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=user, recipe=recipe)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            if Favorite.objects.filter(user=user, recipe=recipe).exists():
                Favorite.objects.get(recipe=recipe).delete()
                return Response(
                    {'errors': 'Рецепт успешно удален из избранного!'},
                    status=status.HTTP_204_NO_CONTENT
                )
        else:
            return Response(
                {'errors': 'Рецепт не был добавлен в избранное!'},
                status=status.HTTP_400_BAD_REQUEST
            )
