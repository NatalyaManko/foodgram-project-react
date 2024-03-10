from django.contrib import admin

<<<<<<< HEAD
from .models import (Favorite,
                     Ingredient,
                     Recipe,
                     RecipeIngredient,
                     RecipeTag,
                     ShoppingCart,
                     Tag)


class IngredientAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'measurement_unit',)
    list_editable = ('measurement_unit',)
    search_fields = ('name',)
    list_filter = ('name',)


class TagAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'slug', 'color',)
    list_editable = ('slug', 'color',)


class RecipeIngredientInline(admin.StackedInline):

    model = RecipeIngredient
    extra = 0


class RecipeTagInline(admin.StackedInline):

    model = RecipeTag
    extra = 0


class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline,
               RecipeTagInline)

    list_display = ('id',
                    'name',
                    'author',
                    'favorite_count')
    search_fields = ('name',)
    list_filter = ('name', 'author', 'tags')
    list_display_links = ('name',)

    def favorite_count(self, obj):
        return obj.favorites.count()

    favorite_count.short_description = 'Число добавлений рецепта в избранное'


=======
from .models import (Ingredient, Tag, Recipe, RecipeIngredient, RecipeTag,
                     ShoppingCart)


class IngredientAdmin(admin.ModelAdmin):
    
    list_display = ('name', 'measurement_unit',)
    list_editable = ('measurement_unit',)
    search_fields = ('name',)
    list_filter = ('name',)
  #  list_display_links = ('name',)
 
    
class TagAdmin(admin.ModelAdmin):
    
    list_display = ('name', 'slug', 'color',)
    list_editable = ('slug', 'color',)
 #   list_display_links = ('name',)


class RecipeAdmin(admin.ModelAdmin):
    
    list_display = ('name',
                    'author')
 #   list_editable = ('text',
 #                   'ingredients',
 #                   'cooking_time',
 #                   'tags')
    search_fields = ('name',)
    list_filter = ('name', 'author', 'tags')
    list_display_links = ('name',)
    filter_horizontal = ('ingredients',)
    
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient)
admin.site.register(RecipeTag)
<<<<<<< HEAD
admin.site.register(ShoppingCart)
admin.site.register(Favorite)
=======
admin.site.register(ShoppingCart)
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
