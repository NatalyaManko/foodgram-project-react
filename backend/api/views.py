import csv
from django.shortcuts import render
from rest_framework import viewsets, filters, status, permissions
#from rest_framework. import IsAuthenticationOrReadOnly, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.throttling import AnonRateThrottle
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
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
from .paginations import PagePagination
from .filters import TagFilter, IngredientFilter, RecipeFilter
from .permissions import (#IsUserOrAuthorOrAdminOrReadOnly,
                          ReadOnly,
                          IsAuthorOrAdminPermission,
                          IsCurrentUserOrOwnerPermission,
                          IsAuthorPermission
                          )



class TagListRetrieve(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAdminUser,)
    pagination_class = None
    filter_baskend = (filters.SearchFilter,)
    filterset_class = TagFilter
    search_fields = ('name',)


class IngredientListRetrieve(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.IsAdminUser,)
    pagination_class = PagePagination
    filter_baskend = (filters.SearchFilter,
                      filters.OrderingFilter)
    filterset_class = IngredientFilter
    search_fields = ('^name',)
    ordering_fields = ('name',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_class = (permissions.IsAuthenticatedOrReadOnly,
                        IsAuthorOrAdminPermission,
                        ReadOnly,)
    throttle_classes = (AnonRateThrottle,)
    throttle_scope = 'travel_speed'
    filter_baskend = (filters.SearchFilter,
                      filters.OrderingFilter)
    filterset_class = RecipeFilter
    search_fields = ('^name',)
    ordering_fields = ('-id',)
    
    def get_serializer_class(self):
        if self.action ==('list', 'retrieve'):
            return RecipeGetSerializer
        return RecipeCreateSerializer

    @action(methods=['post', 'delete'],
            detail=True,
            url_path='shopping_cart',
            permission_classes=[IsCurrentUserOrOwnerPermission])
    def shopping_cart(self, request, **kwargs):
        """
        Получить / Добавить / Удалить  рецепт
        из списка покупок у текущего пользоватля.
        """
        try:
            recipe = Recipe.objects.get(id=self.kwargs.get('pk'))
        except:
            return Response({'errors': 'Объект не найден!'},
                            status=status.HTTP_404_NOT_FOUND)
        user = self.request.user
        if request.method == 'POST':
            serializer = ShoppingCartSerializer(
                data=request.data,
                context={'request': request, 'recipe': recipe})
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=user, recipe=recipe)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
        if ShoppingCart.objects.filter(user=user,
                                       recipe=recipe).exists():
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
            url_path='download_shopping_cart',
            permission_classes=[IsAuthorPermission]) # проверить без него!!!
    def export_shopping_cart(self, request):
        """Отправка csv-файла со списком покупок"""
        shopping_cart_items = (RecipeIngredient.objects.filter(
            recipe__shopping_cart__user=self.request.user).
            prefetch_related('recipe__shopping_card', 'user', 'ingredient').
            values('ingredient__name', 'ingredient__measurement_unit').
            annotate(ingredient_amount=Sum('amount')
                     )
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
                                                'Количество']
                                    )
        writer.writeheader()
        writer.writerows(shopping_cart)
        return response

    @action(methods=['post', 'delete'],
            detail=True,
            url_path='favorite',
            permission_classes=[IsCurrentUserOrOwnerPermission])
    def favourites(self, request, **kwargs):
        """
        Добавить / Удалить  рецепт
        из избранного текущего пользоватля.
        """
        try:
            recipe = Recipe.objects.get(id=self.kwargs.get('pk'))
        except:
            return Response({'errors': 'Объект не найден!'},
                            status=status.HTTP_404_NOT_FOUND)
     #   recipe = get_object_or_404(Recipe, id=self.kwargs.get('pk'))
        user = self.request.user
        if request.method == 'POST':
            serializer = FavoriteSerializer(
                data=request.data,
                context={'request': request, 'recipe': recipe})
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=user, recipe=recipe)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
        if Favorite.objects.filter(user=user,
                                       recipe=recipe).exists():
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