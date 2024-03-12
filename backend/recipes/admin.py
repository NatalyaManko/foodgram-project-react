from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt

from .models import (Favorite,
                     Ingredient,
                     Recipe,
                     RecipeIngredient,
                     RecipeTag,
                     ShoppingCart,
                     Tag)


@csrf_exempt
class IngredientAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'measurement_unit',)
    list_editable = ('measurement_unit',)
    search_fields = ('name',)
    list_filter = ('name',)


@csrf_exempt
class TagAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'slug', 'color',)
    list_editable = ('slug', 'color',)


class RecipeIngredientInline(admin.StackedInline):

    model = RecipeIngredient
    extra = 0


class RecipeTagInline(admin.StackedInline):

    model = RecipeTag
    extra = 0


@csrf_exempt
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline,
               RecipeTagInline,)

    list_display = ('id',
                    'name',
                    'author',
                    'favorite_count')
    list_editable = ('name', 'author',)
    search_fields = ('name',)
    list_filter = ('name', 'author', 'tags')

    def favorite_count(self, obj):
        return obj.favorites.count()

    favorite_count.short_description = 'Число добавлений рецепта в избранное'


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient)
admin.site.register(RecipeTag)
admin.site.register(ShoppingCart)
admin.site.register(Favorite)
