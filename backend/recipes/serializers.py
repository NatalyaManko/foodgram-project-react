import base64

from django.conf import settings
from django.core.files.base import ContentFile
from rest_framework import serializers

from recipes.models import Ingredient, Recipe, RecipeIngredient, UserFavorite
from tags.models import Tag
from tags.serializers import TagSerializer
from users.serializers import UserSerializer


class Base64ImageField(serializers.ImageField):
    """Сериализатор декодирования изображения"""

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr),
                               name='temp.' + ext)

        return super().to_internal_value(data)


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Связной сериализатор Ингредиентов с количеством для Рецептов"""

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit.name')

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class RecipeIngredientSimpleSerializer(serializers.ModelSerializer):
    """Сериализатор Ингредиентов с количеством для создания рецептов"""

    id = serializers.PrimaryKeyRelatedField(
        source='ingredient.id', queryset=Ingredient.objects.all())
    amount = serializers.IntegerField(
        min_value=settings.MIN_SMALL_NUMBER,
        max_value=settings.MAX_SMALL_NUMBER)

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount',)


class RecipeSimpleSerializer(serializers.ModelSerializer):
    """Сериализатор Рецептов для подписок"""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор чтения Рецептa"""

    author = UserSerializer(read_only=True)
    ingredients = RecipeIngredientSerializer(
        source='ingredients_in_recipe', read_only=True, many=True)
    tags = TagSerializer(read_only=True, many=True)

    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = '__all__'

    def get_is_favorited(self, obj):
        if not self.context:
            return False
        user = self.context['request'].user
        return (user.is_authenticated
                and user.favorites.filter(recipe=obj).exists())

    def get_is_in_shopping_cart(self, obj):
        if not self.context:
            return False
        user = self.context['request'].user
        return (user.is_authenticated
                and user.items.filter(recipe=obj).exists())


class RecipeAddChangeSerializer(serializers.ModelSerializer):
    """Сериализатор создания Рецептa"""

    image = Base64ImageField()
    author = UserSerializer(read_only=True)
    ingredients = RecipeIngredientSimpleSerializer(
        source='ingredients_in_recipe', many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True)
    cooking_time = serializers.IntegerField(
        min_value=settings.MIN_SMALL_NUMBER,
        max_value=settings.MAX_SMALL_NUMBER)

    class Meta:
        model = Recipe
        fields = ('name', 'text', 'ingredients', 'image',
                  'cooking_time', 'tags', 'author')

    def create_ingredients(self, recipe, ingredients):
        bulk_list = list()
        for ingredient in ingredients:
            bulk_list.append(RecipeIngredient(
                recipe=recipe,
                ingredient=ingredient['ingredient']['id'],
                amount=ingredient['amount']))
        RecipeIngredient.objects.bulk_create(bulk_list)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients_in_recipe')
        tags = validated_data.pop('tags')

        recipe = Recipe.objects.create(
            author=self.context['request'].user, **validated_data)

        self.create_ingredients(recipe, ingredients)
        recipe.tags.set(tags)

        return recipe

    def update(self, instance, validated_data):

        ingredients = validated_data.pop('ingredients_in_recipe')
        tags = validated_data.pop('tags')
        instance.ingredients.clear()
        instance.tags.clear()

        self.create_ingredients(instance, ingredients)
        instance.tags.set(tags)

        return super().update(instance, validated_data)

    def to_representation(self, value):
        return RecipeSerializer(value).data

    def validate_ingredients(self, value):
        if len(value) < 1:
            raise serializers.ValidationError(
                {'ingredients': 'Должен быть хотя бы один ингредиент'}
            )

        ingredients_arr = []
        for item in value:
            if item in ingredients_arr:
                raise serializers.ValidationError(
                    {'ingredients': 'Ингредиент уже выбран!'}
                )
            ingredients_arr.append(item)

        return value

    def validate_tags(self, value):
        if len(value) < 1:
            raise serializers.ValidationError({'tags': 'Выберите таг.'})

        if len(value) != len(set([tag.id for tag in value])):
            raise serializers.ValidationError(
                {'tags': 'Значения должны быть уникальным.'})

        return value

    def validate(self, obj):
        for field in ('name', 'text', 'cooking_time', 'image',
                      'tags', 'ingredients_in_recipe'):
            if not obj.get(field):
                raise serializers.ValidationError(
                    {f'{field}': f'Поле обязательно: {field}.'}
                )
        ingredients = obj.get('ingredients_in_recipe', [])
        ingredient_ids = set()
        for ingredient in ingredients:
            ingredient_id = ingredient.get('ingredient').get('id')
            if ingredient_id in ingredient_ids:
                raise serializers.ValidationError(
                    {'ingredients_in_recipe':
                        'Ингредиенты должны быть уникальны.'}
                )
            ingredient_ids.add(ingredient_id)

        tags = obj.get('tags', [])
        tag_ids = set(tag.id for tag in tags)
        if len(tags) != len(tag_ids):
            raise serializers.ValidationError(
                {'tags': 'Теги должны быть уникальными.'}
            )

        return obj


class RecipeShoppingSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления и удаления рецепта в Список покупок."""

    class Meta:
        model = Recipe
        fields = '__all__'

    def validate(self, data):
        user = self.context['request'].user
        recipe = self.instance

        if not recipe:
            raise serializers.ValidationError({'recipe': 'Рецепт не найден.'})

        if not user.is_authenticated:
            raise serializers.ValidationError(
                {'user': 'Пользователь не аутентифицирован.'}
            )

        if user.items.filter(recipe=recipe).exists():
            raise serializers.ValidationError(
                {'recipe': f'Рецепт {recipe} уже в списке покупок.'}
            )

        return data


class RecipeFavoriteSerializer(serializers.ModelSerializer):
    """
    Сериализатор для добавления и удаления рецептов
    из Избранного пользователя.
    """

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UserFavorite
        fields = ('user', 'recipe')

    def validate(self, data):
        user = data['user']
        recipe = data['recipe']

        if UserFavorite.objects.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError(
                {'detail': 'Рецепт уже в избранном пользователя.'}
            )

        return data

    def create(self, validated_data):
        user = validated_data['user']
        recipe = validated_data['recipe']
        user_favorite = UserFavorite.objects.create(user=user, recipe=recipe)
        return user_favorite

    def delete(self, instance):
        instance.delete()

    def to_internal_value(self, data):
        try:
            return super().to_internal_value(data)
        except serializers.ValidationError as exc:
            raise serializers.ValidationError({'detail': exc.detail})
