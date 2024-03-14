from colorfield.fields import ColorField
from django.core.validators import MinValueValidator
from django.db import models

from users.models import User


class Ingredient(models.Model):
    """Модель Ингредиента"""

    name = models.CharField('Наименование',
                            max_length=128)
    measurement_unit = models.CharField('Единица измерения',
                                        max_length=50)

    class Meta:
        ordering = ('name',)
        verbose_name = 'ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Tag(models.Model):
    """Модель Тега"""

    name = models.CharField('Название',
                            max_length=128,
                            unique=True)
    slug = models.SlugField('Slug тега',
                            unique=True)
    color = ColorField('Цветовой код',
                       unique=True,
                       max_length=7)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'color'],
                name='unique_tag_color'
            )
        ]
        ordering = ('name',)
        verbose_name = 'тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель Рецепта"""

    name = models.CharField('Название',
                            max_length=200)
    author = models.ForeignKey(User,
                               related_name='recipe',
                               on_delete=models.CASCADE,
                               verbose_name='Автор')
    image = models.ImageField('Картинка',
                              upload_to='recipes/images/')
    text = models.TextField('Описание рецепта')
    ingredients = models.ManyToManyField(Ingredient,
                                         through='RecipeIngredient',
                                         verbose_name='Ингредиент')
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления, мин.',
        validators=[
            MinValueValidator(
                1, message='Время приготовления не может быть меньше 1 минуты'
            )
        ]
    )
    tags = models.ManyToManyField(Tag,
                                  through='RecipeTag',
                                  verbose_name='Тег')

    class Meta:
        ordering = ('-id', 'name', 'author')
        verbose_name = 'рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """Модель Ингредиентов Рецептов"""

    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.CASCADE,
                                   verbose_name='Ингредиент',
                                   related_name='ingredients_amount')
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               verbose_name='Рецепт',
                               related_name='recipes_ingredients')
    amount = models.PositiveSmallIntegerField(
        'Количество ингредиента',
        validators=[
            MinValueValidator(
                1, message='Количество ингредиента не может быть меньше 1'
            )
        ]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredient'
            )
        ]
        ordering = ('-id',)
        verbose_name = 'ингредиент'
        verbose_name_plural = 'Ингредиенты рецептов'

    def __str__(self):
        return f'{self.ingredient} для {self.recipe}'


class RecipeTag(models.Model):
    """Модель Теги Рецептов"""

    tag = models.ForeignKey(Tag,
                            on_delete=models.CASCADE,
                            verbose_name='Тег',
                            related_name='tags')
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               verbose_name='Рецепт',
                               related_name='recipes_tags')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'tag'],
                name='unique_recipe_tag'
            )
        ]
        ordering = ('-id',)
        verbose_name = 'тег'
        verbose_name_plural = 'Теги рецептов'

    def __str__(self):
        return f'{self.tag}: {self.recipe}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name='Пользователь',
                             related_name='shopping_cart')
    recipe = models.ManyToManyField(Recipe,
                                    verbose_name='Список покупок',
                                    related_name='shopping_cart')

    class Meta:
        ordering = ('-id',)
        verbose_name = 'список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self):
        return f'Список покупок {self.user}'


class Favorite(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name='Пользователь',
                             related_name='favorites',
                             )
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               verbose_name='Рецепты',
                               related_name='favorites',
                               )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_favorite_recipe'
            )
        ]
        ordering = ('-id',)
        verbose_name = 'избранные рецепты'
        verbose_name_plural = 'Избранные рецепты'

    def __str__(self):
        return f'Избранные рецепты {self.user}'
