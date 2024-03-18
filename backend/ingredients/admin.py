from django.contrib import admin

from ingredients.models import Ingredient, Unit

admin.site.register(Unit)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit', )
    search_fields = ('name',)
