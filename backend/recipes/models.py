from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from ingredients.models import Ingredient
from tags.models import Tag

User = get_user_model()


class Recipe(models.Model):
    name = models.CharField('Название',
                            max_length=settings.CHAR_FIELD_MAX_LEN)
    text = models.TextField('Описание')
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        validators=(
            MinValueValidator(settings.MIN_SMALL_NUMBER),
            MaxValueValidator(settings.MAX_SMALL_NUMBER),
        ))
    image = models.ImageField('Картинка', upload_to='recipes/')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipes', verbose_name='Автор')
    ingredients = models.ManyToManyField(Ingredient,
                                         through='RecipeIngredient')
    tags = models.ManyToManyField(Tag, through='RecipeTag')

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='ingredients_in_recipe',
                               on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient,
                                   related_name='recipes_have_ingredient',
                                   on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField(
        'Количество', null=False,
        validators=(
            MinValueValidator(settings.MIN_SMALL_NUMBER),
            MaxValueValidator(settings.MAX_SMALL_NUMBER),
        ))

    class Meta:
        ordering = ('recipe__name', 'ingredient__name')
        verbose_name = 'Ингридиента рецепта'
        verbose_name_plural = 'Ингридиенты рецепта'

    def __str__(self):
        return f'{self.recipe} {self.ingredient}'


class RecipeTag(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        ordering = ('recipe__name', 'tag__name')
        verbose_name = 'Таг рецепта'
        verbose_name_plural = 'Таги рецепта'

    def __str__(self):
        return f'{self.recipe} {self.tag}'


class UserFavorite(models.Model):
    user = models.ForeignKey(User, related_name='favorites',
                             on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, related_name='users_like_recipe',
                               on_delete=models.CASCADE)

    class Meta:
        ordering = ('user__username', 'recipe__name')
        verbose_name = 'Любимый рецепт'
        verbose_name_plural = 'Любимые рецепты'

    def __str__(self):
        return f'{self.user} любит {self.recipe}'


class UserShoppingCart(models.Model):
    user = models.ForeignKey(User, related_name='items',
                             on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, related_name='users_add_recipe',
                               on_delete=models.CASCADE)

    class Meta:
        ordering = ('user__username', 'recipe__name')
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self):
        return f'{self.user} купит {self.recipe}'
