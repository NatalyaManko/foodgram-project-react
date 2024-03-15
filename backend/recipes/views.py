from collections import defaultdict

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from recipes.filters import RecipeFilter
from recipes.models import (Recipe,
                            RecipeIngredient,
                            UserFavorite,
                            UserShoppingCart)
from recipes.permissions import IsOwnerOrReadOnly
from recipes.serializers import (RecipeAddChangeSerializer,
                                 RecipeSerializer,
                                 RecipeSimpleSerializer)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, )
    search_fields = ('^name', )
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return RecipeAddChangeSerializer
        return RecipeSerializer

    @action(('post', 'delete'), detail=True,
            permission_classes=(IsAuthenticated,))
    def favorite(self, request, **kwargs):
        user = request.user

        if request.method == 'POST':
            try:
                recipe = Recipe.objects.get(id=kwargs['pk'])
            except ObjectDoesNotExist as inst:
                raise serializers.ValidationError(inst)

            if user.favorites.filter(recipe=recipe):
                return Response({'errors':
                                 f'Рецепт {recipe} уже в избранном.'},
                                status=status.HTTP_400_BAD_REQUEST)
            UserFavorite.objects.create(user=user, recipe=recipe)
            serializer = RecipeSimpleSerializer(recipe)

            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)

        else:
            recipe = get_object_or_404(Recipe, id=kwargs['pk'])

            try:
                UserFavorite.objects.get(user=user, recipe=recipe).delete()
            except ObjectDoesNotExist as inst:
                raise serializers.ValidationError(inst)

            return Response({'detail': 'OK'},
                            status=status.HTTP_204_NO_CONTENT)

    @action(('post', 'delete'), detail=True,
            permission_classes=(IsAuthenticated,))
    def shopping_cart(self, request, **kwargs):
        user = request.user

        if request.method == 'POST':
            try:
                recipe = Recipe.objects.get(id=kwargs['pk'])
            except ObjectDoesNotExist as inst:
                raise serializers.ValidationError(inst)

            if user.items.filter(recipe=recipe):
                return Response({'errors':
                                 f'Рецепт {recipe} уже в списке покупок.'},
                                status=status.HTTP_400_BAD_REQUEST)
            UserShoppingCart.objects.create(user=user, recipe=recipe)
            serializer = RecipeSimpleSerializer(recipe)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            recipe = get_object_or_404(Recipe, id=kwargs['pk'])
            try:
                UserShoppingCart.objects.get(user=user, recipe=recipe).delete()
            except ObjectDoesNotExist as inst:
                raise serializers.ValidationError(inst)

            return Response({'detail': 'OK'},
                            status=status.HTTP_204_NO_CONTENT)

    @action(('get',), detail=False, permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):

        ingredients_list = RecipeIngredient.objects.filter(
            recipe__users_add_recipe__user=request.user)

        shopping_items = defaultdict(int)

        for ingredient in ingredients_list:
            shopping_items[ingredient.ingredient] += ingredient.amount

        shopping_items_text = 'СПИСОК ПОКУПОК:\n'
        shopping_items_text += '\n'.join([f'{i+1}. '
                                         + f'{ingredient.name} - '
                                         + f'{shopping_items[ingredient]}, '
                                         + f'{ingredient.measurement_unit}'
                                         for i, ingredient
                                         in enumerate(shopping_items.keys())])

        response = HttpResponse(shopping_items_text,
                                content_type='text/plain,charset=utf8')
        response['Content-Disposition'] = 'attachment; filename=file.txt'

        return response
