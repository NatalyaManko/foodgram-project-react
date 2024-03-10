import csv
<<<<<<< HEAD

from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.db.models import Sum
from django.http import HttpResponse
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
from .permissions import IsAuthorPermission, IsAdminOrReadOnlyPermission, IsAdminPermission
from .serializers import (FavoriteSerializer,
                          IngredientSerializer,
                          RecipeCreateSerializer,
                          RecipeGetSerializer,
                          ShoppingCartSerializer,
                          TagSerializer)
=======
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

>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3


class TagListRetrieve(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
<<<<<<< HEAD
  #  permission_classes = (IsAdminOrReadOnlyPermission,)
    pagination_class = None
    filter_baskend = (filters.SearchFilter,)
    filterset_class = TagFilter
    search_fields = ('name')
=======
    permission_classes = (permissions.IsAdminUser,)
    pagination_class = None
    filter_baskend = (filters.SearchFilter,)
    filterset_class = TagFilter
    search_fields = ('name',)
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3


class IngredientListRetrieve(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
<<<<<<< HEAD
 #   permission_classes = (IsAdminOrReadOnlyPermission,)
    pagination_class = None
=======
    permission_classes = (permissions.IsAdminUser,)
    pagination_class = PagePagination
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
    filter_baskend = (filters.SearchFilter,
                      filters.OrderingFilter)
    filterset_class = IngredientFilter
    search_fields = ('^name',)
    ordering_fields = ('name',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
<<<<<<< HEAD
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorPermission,
  #      IsAdminPermission,
    )
    pagination_class = LimitOffsetPagination
=======
    permission_class = (permissions.IsAuthenticatedOrReadOnly,
                        IsAuthorOrAdminPermission,
                        ReadOnly,)
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
    throttle_classes = (AnonRateThrottle,)
    throttle_scope = 'travel_speed'
    filter_baskend = (filters.SearchFilter,
                      filters.OrderingFilter)
    filterset_class = RecipeFilter
    search_fields = ('^name',)
    ordering_fields = ('-id',)
<<<<<<< HEAD

    def get_serializer_class(self):
        if self.action == ('list', 'retrieve'):
            return RecipeGetSerializer
        return RecipeCreateSerializer

    def perform_update(self, serializer, **kwargs):
        user = self.request.user
        if Recipe.objects.get(id=self.kwargs.get('pk')).author != user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(RecipeViewSet, self).perform_update(serializer)

    def perform_destroy(self, serializer, **kwargs):
        user = self.request.user
        try:
            Recipe.objects.get(id=self.kwargs.get('pk'), author=user).delete()
            return Response('Успешное удаление!',
                            status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            if Recipe.objects.get(id=self.kwargs.get('pk')).author != user:
                raise PermissionDenied('Изменение чужого контента запрещено!')
            else:
                return Response({'errors': 'Рецепт не найден!'},
                                status=status.HTTP_404_NOT_FOUND)

    @action(methods=['post', 'delete'],
            detail=True,
            url_path='shopping_cart',
            permission_classes=[permissions.IsAuthenticated])
=======
    
    def get_serializer_class(self):
        if self.action ==('list', 'retrieve'):
            return RecipeGetSerializer
        return RecipeCreateSerializer

    @action(methods=['post', 'delete'],
            detail=True,
            url_path='shopping_cart',
            permission_classes=[IsCurrentUserOrOwnerPermission])
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
    def shopping_cart(self, request, **kwargs):
        """
        Получить / Добавить / Удалить  рецепт
        из списка покупок у текущего пользоватля.
        """
<<<<<<< HEAD
        user = self.request.user
        if request.method == 'POST':
            try:
                recipe = Recipe.objects.get(id=self.kwargs.get('pk'))
            except ObjectDoesNotExist:
                return Response({'errors': 'Рецепт не найден!'},
                                status=status.HTTP_400_BAD_REQUEST)
            if ShoppingCart.objects.filter(user=user,
                                           recipe=recipe).exists():
                return Response(
                    {'errors': 'Рецепт уже добавлен в список покупок!'},
                    status=status.HTTP_400_BAD_REQUEST
                )
=======
        try:
            recipe = Recipe.objects.get(id=self.kwargs.get('pk'))
        except:
            return Response({'errors': 'Объект не найден!'},
                            status=status.HTTP_404_NOT_FOUND)
        user = self.request.user
        if request.method == 'POST':
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
            serializer = ShoppingCartSerializer(
                data=request.data,
                context={'request': request, 'recipe': recipe})
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=user, recipe=recipe)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
<<<<<<< HEAD
        elif request.method == 'DELETE':
            try:
                recipe = Recipe.objects.get(id=self.kwargs.get('pk'))
            except ObjectDoesNotExist:
                return Response({'errors': 'Рецепт не найден!'},
                                status=status.HTTP_404_NOT_FOUND)

=======
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
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
<<<<<<< HEAD
                status=status.HTTP_400_BAD_REQUEST
            )
=======
                 status=status.HTTP_400_BAD_REQUEST
                 )
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3

    @action(methods=['get'],
            detail=False,
            url_path='download_shopping_cart',
<<<<<<< HEAD
            permission_classes=[IsAuthorPermission])
=======
            permission_classes=[IsAuthorPermission]) # проверить без него!!!
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
    def export_shopping_cart(self, request):
        """Отправка csv-файла со списком покупок"""
        shopping_cart_items = (RecipeIngredient.objects.filter(
            recipe__shopping_cart__user=self.request.user).
            prefetch_related('recipe__shopping_card', 'user', 'ingredient').
            values('ingredient__name', 'ingredient__measurement_unit').
<<<<<<< HEAD
            annotate(ingredient_amount=Sum('amount'))
        )
=======
            annotate(ingredient_amount=Sum('amount')
                     )
            )
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
        shopping_cart = []
        for item in shopping_cart_items:
            shopping_cart.append({
                'Название': item['ingredient__name'],
                'Единица измерения': item['ingredient__measurement_unit'],
                'Количество': item['ingredient_amount'],
            })
<<<<<<< HEAD

=======
  
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = \
            'attachment; filename="shopping_cart.csv"'
        writer = csv.DictWriter(response,
<<<<<<< HEAD
                                fieldnames=['Название',
                                            'Единица измерения',
                                            'Количество'])
=======
                                    fieldnames=['Название',
                                                'Единица измерения',
                                                'Количество']
                                    )
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
        writer.writeheader()
        writer.writerows(shopping_cart)
        return response

    @action(methods=['post', 'delete'],
            detail=True,
            url_path='favorite',
<<<<<<< HEAD
            permission_classes=[permissions.IsAuthenticated]
            )
=======
            permission_classes=[IsCurrentUserOrOwnerPermission])
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
    def favourites(self, request, **kwargs):
        """
        Добавить / Удалить  рецепт
        из избранного текущего пользоватля.
        """
<<<<<<< HEAD
        user = self.request.user
        if request.method == 'POST':
            try:
                recipe = Recipe.objects.get(id=self.kwargs.get('pk'))
            except ObjectDoesNotExist:
                return Response({'errors': 'Объект не найден!'},
                                status=status.HTTP_400_BAD_REQUEST)
            if Favorite.objects.filter(user=user,
                                       recipe=recipe).exists():
                return Response({'errors': 'Рецепт уже добавлен в избранное!'},
                                status=status.HTTP_400_BAD_REQUEST)
=======
        try:
            recipe = Recipe.objects.get(id=self.kwargs.get('pk'))
        except:
            return Response({'errors': 'Объект не найден!'},
                            status=status.HTTP_404_NOT_FOUND)
     #   recipe = get_object_or_404(Recipe, id=self.kwargs.get('pk'))
        user = self.request.user
        if request.method == 'POST':
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
            serializer = FavoriteSerializer(
                data=request.data,
                context={'request': request, 'recipe': recipe})
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=user, recipe=recipe)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
<<<<<<< HEAD
        elif request.method == 'DELETE':
            try:
                recipe = Recipe.objects.get(id=self.kwargs.get('pk'))
            except ObjectDoesNotExist:
                return Response({'errors': 'Рецепт не найден!'},
                                status=status.HTTP_404_NOT_FOUND)

        if Favorite.objects.filter(user=user,
                                   recipe=recipe).exists():
=======
        if Favorite.objects.filter(user=user,
                                       recipe=recipe).exists():
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
            Favorite.objects.get(recipe=recipe).delete()
            return Response(
                {'errors': 'Рецепт успешно удален из избранного!'},
                status=status.HTTP_204_NO_CONTENT
            )
        else:
            return Response(
                {'errors': 'Рецепт не был добавлен в избранное!'},
<<<<<<< HEAD
                status=status.HTTP_400_BAD_REQUEST
            )
=======
                 status=status.HTTP_400_BAD_REQUEST
                 )
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
