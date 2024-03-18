from collections import defaultdict
from datetime import datetime

from django.http import HttpResponse

from recipes.models import RecipeIngredient


def download_shopping_cart(request):
    """
    Скачать список покупок в виде текстового файла.
    Возвращает:
        HttpResponse: Ответ с текстовым файлом для скачивания.
    """
    ingredients_list = RecipeIngredient.objects.filter(
        recipe__users_add_recipe__user=request.user
    )

    shopping_items = defaultdict(int)

    for ingredient in ingredients_list:
        shopping_items[ingredient.ingredient] += ingredient.amount

    current_datetime = datetime.now()
    current_datetime_str = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

    shopping_items_text = f'СПИСОК ПОКУПОК (от: {current_datetime_str}):\n'

    shopping_items_text += '\n'.join(
        [
            (f'{i+1}. {ingredient.name} - '
             + f'{shopping_items[ingredient]}, '
             + f'{ingredient.measurement_unit}')
            for i, ingredient in enumerate(shopping_items.keys())
        ]
    )

    response = HttpResponse(
        shopping_items_text, content_type='text/plain,charset=utf8')
    response['Content-Disposition'] = 'attachment; filename=file.txt'

    return response
