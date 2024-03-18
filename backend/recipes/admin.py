from django.contrib import admin

from recipes.models import (Recipe,
                            RecipeIngredient,
                            RecipeTag,
                            UserFavorite,
                            UserShoppingCart)


class RecipeTagInline(admin.TabularInline):
    model = RecipeTag
    extra = 0
    min_num = 1


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    fields = ('ingredient', 'amount', 'ingredient__measurement_unit')
    extra = 0
    min_num = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline, RecipeTagInline,)
    list_display = ('name', 'author', 'favorites_count')
    search_fields = ('name', 'author', 'tags')
    readonly_fields = ('favorites_count',)

    @admin.display(description='Любимые рецепты')
    def favorites_count(self, obj):
        return obj.users_like_recipe.count()


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
