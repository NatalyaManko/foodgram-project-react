from django.forms.fields import CharField
from django_filters import CharFilter, FilterSet, ModelMultipleChoiceFilter
from django_filters.fields import MultipleChoiceField
from django_filters.filters import Filter, NumberFilter

from recipes.models import Ingredient, Recipe, Tag
from users.models import User


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
        fields = {'name': ['contains']}


class IngredientFilter(FilterSet):

    name = CharFilter(field_name='name', label='Ингредиент')

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(FilterSet):

    author = ModelMultipleChoiceFilter(queryset=User.objects.all(),
                                       field_name='author__username',
                                       lookup_expr='icontains',
                                       label='Имя автора')
    tags = ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )
    is_favorited = NumberFilter(method='filter_is_favorited')
    is_in_shopping_cart = NumberFilter(method='filter_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ('author',
                  'tags',
                  'is_favorited',
                  'is_in_shopping_cart',)

    def filter_is_favorited(self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            return queryset.filter(shopping_cart__user=self.request.user)
        return queryset
