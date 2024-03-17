from django.contrib import admin, messages

from recipes.models import (Recipe,
                            RecipeIngredient,
                            RecipeTag,
                            UserFavorite,
                            UserShoppingCart)


class RecipeIngredientInline(admin.StackedInline):
    model = RecipeIngredient
    extra = 0


class RecipeTagInline(admin.StackedInline):
    model = RecipeTag
    extra = 0


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline,
               RecipeTagInline,)
    list_display = ('id',
                    'name',
                    'author',)
    list_editable = ('name', 'author',)
    search_fields = ('name',)
    list_filter = ('name', 'author', 'tags')
    readonly_fields = ('favorites_count',)

    @admin.display(description='Любим')
    def favorites_count(self, obj):
        return obj.users_like_recipe.count()

    def save_model(self, request, obj, form, change):
        if not obj.name:
            messages.error(request, 'Пожалуйста, заполните поле "Название".')
            return

        if not obj.ingredients.exists():
            messages.error(
                request,
                'Пожалуйста, добавьте хотя бы один ингредиент к рецепту.'
            )
            return

        if not obj.tags.exists():
            messages.error(
                request,
                'Пожалуйста, добавьте хотя бы один тег к рецепту.'
            )
            return

        super().save_model(request, obj, form, change)
        messages.success(request, 'Рецепт успешно создан.')


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
