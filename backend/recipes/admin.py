from django.contrib import admin

from recipes.models import (Recipe,
                            RecipeIngredient,
                            RecipeTag,
                            UserFavorite,
                            UserShoppingCart)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author',)
    list_filter = ('name', 'tags', 'author')
    readonly_fields = ('favorites_count',)

    @admin.display(description='Любим')
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
