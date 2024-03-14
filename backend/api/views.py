import csv

from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
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
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = None
    filter_baskend = (DjangoFilterBackend, filters.SearchFilter,)
    filterset_class = TagFilter
    search_fields = ('name')


class IngredientListRetrieve(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = None
    filter_baskend = (filters.SearchFilter,
                      filters.OrderingFilter)
    filterset_class = IngredientFilter
    search_fields = ('^name',)
    ordering_fields = ('name',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorPermission,
    )
    pagination_class = LimitOffsetPagination
    throttle_classes = (AnonRateThrottle,)
    throttle_scope = 'travel_speed'
    filter_baskend = (filters.SearchFilter,
                      filters.OrderingFilter)
    filterset_class = RecipeFilter
    search_fields = ('^name',)
    ordering_fields = ('-id',)

    def get_serializer_class(self):
        if self.action == ('list', 'retrieve'):
            return RecipeGetSerializer
        return RecipeCreateSerializer

    def perform_update(self, serializer, **kwargs):
        user = self.request.user
        if Recipe.objects.get(id=self.kwargs.get('pk')).author != user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        user = self.request.user
        try:
            recipe = Recipe.objects.get(id=self.kwargs.get('pk'))
            if recipe.author != user:
                raise PermissionDenied(
                    'У вас нет прав для удаления этого рецепта.'
                )
            recipe.delete()
            return Response('Успешное удаление!',
                            status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response({'errors': 'Рецепт не найден!'},
                            status=status.HTTP_404_NOT_FOUND)

    @action(methods=['post', 'delete'],
            detail=True,
            url_path='favorite',
            permission_classes=[permissions.IsAuthenticated])
    def favourites(self, request, **kwargs):
        """
        Добавить / Удалить  рецепт
        из избранного текущего пользоватля.
        """
        user = self.request.user
        try:
            recipe = Recipe.objects.get(id=self.kwargs.get('pk'))
        except Recipe.DoesNotExist:
            return Response({'errors': 'Рецепт не найден!'},
                            status=status.HTTP_404_NOT_FOUND)

        if request.method == 'POST':
            if Favorite.objects.filter(user=user, recipe=recipe).exists():
                return Response({'errors': 'Рецепт уже добавлен в избранное!'},
                                status=status.HTTP_400_BAD_REQUEST)
            serializer = FavoriteSerializer(
                data=request.data,
                context={'request': request, 'recipe': recipe}
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=user, recipe=recipe)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            favorite_instance = Favorite.objects.filter(
                user=user, recipe=recipe
            ).first()
            if favorite_instance:
                favorite_instance.delete()
                return Response(
                    {'message': 'Рецепт успешно удален из избранного!'},
                    status=status.HTTP_204_NO_CONTENT
                )
            else:
                return Response(
                    {'errors': 'Рецепт не был добавлен в избранное!'},
                    status=status.HTTP_400_BAD_REQUEST
                )


class ShoppingCartViewSet(viewsets.ModelViewSet):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True,
            methods=['post'])
    def add_to_cart(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        if ShoppingCart.objects.filter(user=request.user,
                                       recipe=recipe).exists():
            return Response({'message': 'Рецепт уже в корзине!'},
                            status=status.HTTP_400_BAD_REQUEST)
        shopping_cart = ShoppingCart.objects.create(user=request.user,
                                                    recipe=recipe)
        serializer = self.get_serializer(shopping_cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True,
            methods=['delete'])
    def remove_from_cart(self, request, pk=None):
        shopping_cart = self.get_object()
        if shopping_cart.user != request.user:
            return Response({'error': 'У вас нет прав для удаления!'},
                            status=status.HTTP_403_FORBIDDEN)
        shopping_cart.delete()
        return Response({'message': 'Рецепт удален из корзины!'},
                        status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'],
            detail=False,
            url_path='download_shopping_cart')
    def export_shopping_cart(self, request):
        """Отправка csv-файла со списком покупок"""
        shopping_cart_items = (RecipeIngredient.objects.filter(
            recipe__shopping_cart__user=self.request.user).
            prefetch_related('recipe__shopping_card', 'user', 'ingredient').
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
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = \
            'attachment; filename="shopping_cart.csv"'
        writer = csv.DictWriter(response,
                                fieldnames=['Название',
                                            'Единица измерения',
                                            'Количество'])
        writer.writeheader()
        writer.writerows(shopping_cart)
        return response
