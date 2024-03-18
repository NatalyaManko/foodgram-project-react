from django.contrib import admin, messages
from django.core.exceptions import ValidationError

from recipes.models import (Recipe,
                            RecipeIngredient,
                            RecipeTag,
                            UserFavorite,
                            UserShoppingCart)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


class RecipeTagInline(admin.TabularInline):
    model = RecipeTag
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline, RecipeTagInline,)
    list_display = ('name', 'author',)
    search_fields = ('name', 'author', 'tags')
    readonly_fields = ('favorites_count',)

    @admin.display(description='Любимые рецепты')
    def favorites_count(self, obj):
        return obj.users_like_recipe.count()

    def save_model(self, request, obj, form, change):
        try:
            obj.full_clean()
        except ValidationError as e:
            messages.error(
                request, "Ошибка сохранения: {}".format(e.message)
            )
            return
        super().save_model(request, obj, form, change)


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')


@admin.register(RecipeTag)
class RecipeTagAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'tag')


@admin.register(UserFavorite)
class UserFavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


@admin.register(UserShoppingCart)
class UserShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
