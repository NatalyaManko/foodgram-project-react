from django.contrib import admin

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
    
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient)
admin.site.register(RecipeTag)
admin.site.register(ShoppingCart)
