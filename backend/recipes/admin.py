from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from recipes.models import (Recipe,
                            RecipeIngredient,
                            RecipeTag,
                            UserFavorite,
                            UserShoppingCart)


class RecipeIngredientFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()

        ingredient_ids = set()
        for form in self.forms:
            if form.cleaned_data:
                ingredient_id = form.cleaned_data['ingredient'].id
                if ingredient_id in ingredient_ids:
                    raise ValidationError(
                        'Ингредиенты должны быть уникальными.'
                    )
                ingredient_ids.add(ingredient_id)

        for form in self.forms:
            if form.cleaned_data:
                if (not form.cleaned_data['ingredient']
                        or not form.cleaned_data['amount']):
                    raise ValidationError(
                        'Пожалуйста, заполните все обязательные поля.'
                    )


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    formset = RecipeIngredientFormSet


class RecipeTagFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()

        for form in self.forms:
            if form.cleaned_data:
                if not form.cleaned_data['tag']:
                    raise ValidationError(
                        'Пожалуйста, выберите тег для всех рецептов.'
                    )

        tag_ids = set()
        for form in self.forms:
            if form.cleaned_data:
                tag_id = form.cleaned_data['tag'].id
                if tag_id in tag_ids:
                    raise ValidationError('Теги должны быть уникальными.')
                tag_ids.add(tag_id)


class RecipeTagInline(admin.TabularInline):
    model = RecipeTag
    extra = 1
    formset = RecipeTagFormSet


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline,
               RecipeTagInline,)
    list_display = ('name',
                    'author',)
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
                request, "Ошибка сохранения: {}".format(e.message_dict)
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
