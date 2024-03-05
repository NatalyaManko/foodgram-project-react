from django_filters import FilterSet, CharFilter, ModelMultipleChoiceFilter
from django_filters.fields import MultipleChoiceField

from django_filters.filters import Filter
from recipes.models import Tag, Ingredient, Recipe, Favorite, ShoppingCart
from django.forms.fields import CharField


class MultipleValueField(MultipleChoiceField):

    def __init__(self, *args, field_class, **kwargs):
        self.inner_field = field_class()
        super().__init__(*args, **kwargs)

    def valid_value(self, value):
        return self.inner_field.validate(value)

    def clean(self, values):
        return values and [self.inner_field.clean(value) for value in values]


class MultipleValueFilter(Filter):

    field_class = MultipleValueField

    def __init__(self, *args, field_class, **kwargs):
        kwargs.setdefault('lookup_expr', 'in')
        super().__init__(*args, field_class=field_class, **kwargs)


class TagFilter(FilterSet):

    name = MultipleValueFilter(field_class=CharField)

    class Meta:
        model = Tag
        fields = ('name',)


class IngredientFilter(FilterSet):
    
    name = CharFilter(field_name='name', label='Ингредиент')
   
    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(FilterSet):

    author = CharFilter(field_name='author__username',
                                      lookup_expr='icontains',
                                      label='Имя автора')
    tags = CharFilter(field_name='tags__name',
                      lookup_expr='exact',
                      label='Тег')
    favorites = ModelMultipleChoiceFilter(queryset=Favorite.objects.all(),
                                          field_name='favorites',
                                          label='Избранное')
    shopping_cart = ModelMultipleChoiceFilter(
        queryset=ShoppingCart.objects.all(),
        field_name='shopping_cart',
        label='Список покупок'
        )

    class Meta:
        model = Recipe
        fields = ('favorites',
                  'author',
                  'tags',
                  'shopping_cart',)