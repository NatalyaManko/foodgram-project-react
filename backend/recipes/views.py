from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from recipes.filters import RecipeFilter
from recipes.models import (Recipe,
                            RecipeIngredient,
                            UserFavorite,
                            UserShoppingCart)
from recipes.serializers import (RecipeAddChangeSerializer,
                                 RecipeSerializer,
                                 RecipeSimpleSerializer)

from .utils import generate_shopping_list


class RecipeViewSet(viewsets.ModelViewSet):
    """
    API endpoint для просмотра, создания, обновления и удаления рецептов.
    """

    queryset = Recipe.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, )
    search_fields = ('^name', )
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        """
        Получить класс сериализатора в зависимости от типа запроса.
        Возвращает:
            Класс сериализатора.
        """
        if self.request.method in ('POST', 'PATCH'):
            return RecipeAddChangeSerializer
        return RecipeSerializer

    def perform_update(self, serializer, **kwargs):
        """
        Выполнить обновление рецепта.
        """
        user = self.request.user
        if Recipe.objects.get(id=self.kwargs.get('pk')).author != user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        """
        Выполнить удаление рецепта.
        """
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

    @action(('post', 'delete'), detail=True,
            permission_classes=(IsAuthenticated,))
    def favorite(self, request, **kwargs):
        """
        Добавить рецепт в избранное или удалить из избранного.
        Возвращает:
            Ответ с данными о рецепте или информацией об успешном удалении.
        """
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
        """
        Добавить рецепт в список покупок или удалить из списка покупок.
        Возвращает:
            Ответ с данными о рецепте или информацией об успешном удалении.
        """
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
        """
        Скачать список покупок в виде текстового файла.
        Возвращает:
        HttpResponse: Ответ с текстовым файлом для скачивания.
        """
        ingredients_list = RecipeIngredient.objects.filter(
            recipe__users_add_recipe__user=request.user
        )

        shopping_items_text = generate_shopping_list(ingredients_list)

        response = HttpResponse(shopping_items_text,
                                content_type='text/plain,charset=utf8')
        response['Content-Disposition'] = 'attachment; filename=file.txt'

        return response
