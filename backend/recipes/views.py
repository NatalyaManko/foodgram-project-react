from backend.permissions import IsAuthorPermission
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from recipes.filters import RecipeFilter
from recipes.models import Recipe, UserFavorite, UserShoppingCart
from recipes.serializers import (RecipeAddChangeSerializer,
                                 RecipeFavoriteSerializer,
                                 RecipeSerializer,
                                 RecipeShoppingSerializer)
from recipes.utils import download_shopping_cart


class RecipeViewSet(viewsets.ModelViewSet):
    """
    API endpoint для просмотра, создания, обновления и удаления рецептов.
    """

    queryset = Recipe.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsAuthorPermission)
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

    @action(('post', 'delete'), detail=True,
            permission_classes=(IsAuthenticated,))
    def favorite(self, request, **kwargs):
        """
        Добавить рецепт в избранное или удалить из избранного.
        Возвращает:
            Ответ с данными о рецепте или информацией об успешном удалении.
        """
        user = request.user
        recipe = self.get_object()

        try:
            favorite_item = UserFavorite.objects.get(user=user, recipe=recipe)
        except UserFavorite.DoesNotExist:
            favorite_item = None

        serializer = RecipeFavoriteSerializer(
            instance=favorite_item,
            data={'user': user.pk, 'recipe': recipe.pk},
            context={'request': request, 'user': user}
        )

        serializer.is_valid(raise_exception=True)
        if request.method == 'POST':
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            serializer.delete()
            return Response(
                {'detail': 'OK'}, status=status.HTTP_204_NO_CONTENT
            )

    @action(('post', 'delete'), detail=True,
            permission_classes=(IsAuthenticated,))
    def shopping_cart(self, request, **kwargs):
        """
        Добавить рецепт в список покупок или удалить из списка покупок.
        Возвращает:
            Ответ с данными о рецепте или информацией об успешном удалении.
        """
        user = request.user
        recipe = self.get_object()

        if request.method == 'POST':
            UserShoppingCart.objects.create(user=user, recipe=recipe)
            serializer = RecipeShoppingSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            shopping_cart_item = get_object_or_404(
                UserShoppingCart, user=user, recipe=recipe
            )
            shopping_cart_item.delete()
            return Response(
                {'detail': 'OK'}, status=status.HTTP_204_NO_CONTENT
            )

    @action(('get',), detail=False, permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        """
        Скачать список покупок в виде текстового файла.
        Возвращает:
        HttpResponse: Ответ с текстовым файлом для скачивания.
        """

        return download_shopping_cart(request)
