# Generated by Django 3.2.3 on 2024-03-01 03:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipeingredient',
            options={'ordering': ('recipe__name', 'ingredient__name'), 'verbose_name': 'Ингридиента рецепта', 'verbose_name_plural': 'Ингридиенты рецепта'},
        ),
        migrations.AlterModelOptions(
            name='recipetag',
            options={'ordering': ('recipe__name', 'tag__name'), 'verbose_name': 'Таг рецепта', 'verbose_name_plural': 'Таги рецепта'},
        ),
        migrations.AlterModelOptions(
            name='userfavorite',
            options={'ordering': ('user__username', 'recipe__name'), 'verbose_name': 'Любимый рецепт', 'verbose_name_plural': 'Любимые рецепты'},
        ),
        migrations.AlterModelOptions(
            name='usershoppingcart',
            options={'ordering': ('user__username', 'recipe__name'), 'verbose_name': 'Список покупок', 'verbose_name_plural': 'Списки покупок'},
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(32000)], verbose_name='Время приготовления'),
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='amount',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(32000)], verbose_name='Количество'),
        ),
    ]